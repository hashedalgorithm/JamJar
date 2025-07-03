from typing import Any
from bcc import BPF
from utils.helper import get_username_by_uid
from core.process_tracer import ProcessTracer, Process
from core.subroutines import Subroutines


class EBPF:

    def __init__(self, ebpf_path: str):
        self.process_tracer = ProcessTracer()
        self.bpf = BPF(text=self.load_bpf_c_code(ebpf_path))
        self.subroutines = Subroutines(self.process_tracer)
        self.perf_buffer_name = "syscall_trigger_events"

        # Hooking into Security BRPM Creds for Exec
        self.bpf.attach_kprobe(
            event="security_bprm_creds_for_exec", fn_name="trace_creds_for_exec"
        )

    def load_bpf_c_code(self, ebpf_path: str) -> str:
        try:
            with open(ebpf_path, "r") as f:
                bpf_source = f.read()
                return bpf_source
        except FileNotFoundError:
            print(f"[!] Could not find eBPF source file at {ebpf_path}.")
            print(f"[!] Exiting...")
            exit(1)

    def intialize_hook_points(self):
        self.bpf[self.perf_buffer_name].open_perf_buffer(self.syscall_trigger_callback)

    def get_perf_buffer_events(self, data: Any) -> list[Any]:
        return self.bpf[self.perf_buffer_name].event(data)

    def syscall_trigger_callback(self, cpu: int, data: Any, size: int) -> None:
        event = self.get_perf_buffer_events(data)

        if event.pid in self.process_tracer.attached_processes:
            print(f"[!] Process already been paused -  {event.pid}.")
            return

        process = self.process_tracer.attach(event.pid)
        self.handle_attached_process(process)

    def handle_attached_process(self, process: Process):

        full_command = process.get_full_command(process.pid)
        command = process.get_command(process.pid)
        tty = process.get_tty(process.pid)
        uid = process.get_uid(process.pid)
        ppid = process.get_ppid(process.pid)
        username = get_username_by_uid(uid)

        self.event_handler(
            process.pid,
            ppid,
            command,
            full_command,
            tty,
            username,
        )

    def event_handler(
        self,
        pid: int,
        ppid: int,
        command: str,
        full_command: str,
        tty: str,
        username: str,
    ) -> None:
        match command:
            case "cd" | "ls" | "rmdir" | "mkdir" | "mv" | "cp" | "rm":
                return self.subroutines.directory_routine(
                    pid, ppid, command, full_command
                )

            case "ifconfig" | "nmap" | "ping" | "arp" | "ip" | "traceroute" | "ftp":
                return self.subroutines.network_routine(
                    pid, ppid, command, full_command
                )

            case "ps" | "kill" | "killall":
                return self.subroutines.process_routine(
                    pid, ppid, full_command, tty, username
                )

            case (
                "cat"
                | "grep"
                | "echo"
                | "locate"
                | "wget"
                | "curl"
                | "unzip"
                | "chmod"
                | "nano"
                | "pico"
                | "vi"
                | "vim"
                | "ln"
                | "crontab"
            ):
                return self.subroutines.file_ops_routine(command, full_command)

            case (
                "df"
                | "history"
                | "php"
                | "uname"
                | "whoami"
                | "w"
                | "id"
                | "last"
                | "uptime"
            ):
                return self.subroutines.system_routine(command, full_command)

            case _:
                print(f"[!] Subroutine for command {command} is not implemented yet!")
                return
