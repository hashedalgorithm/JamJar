from typing import Any
from bcc import BPF
from utils.helper import get_username_by_uid
from core.process_tracer import ProcessTracer, Process
from core.subroutines import Subroutines
from utils.logger import Logger


class EBPF(Logger):

    def __init__(self, ebpf_path: str):
        super().__init__()
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
            self.logger.fatal(f"Could not find eBPF source file at {ebpf_path}.")
            exit(1)

    def intialize_hook_points(self):
        self.bpf[self.perf_buffer_name].open_perf_buffer(self.syscall_trigger_callback)

    def get_perf_buffer_events(self, data: Any) -> list[Any]:
        return self.bpf[self.perf_buffer_name].event(data)

    def syscall_trigger_callback(self, cpu: int, data: Any, size: int) -> None:
        event = self.get_perf_buffer_events(data)

        if event.pid in self.process_tracer.attached_processes:
            self.logger.warning(f"Process already been paused -  {event.pid}.")
            return

        process = self.process_tracer.attach(event.pid)
        self.handle_attached_process(process)

    def handle_attached_process(self, process: Process):

        username = get_username_by_uid(process.uid)

        self.event_handler(
            process,
            username,
        )

    def event_handler(
        self,
        process: Process,
        username: str,
    ) -> None:
        match process.command:
            case "cd" | "ls" | "rmdir" | "mkdir" | "mv" | "cp" | "rm":
                return self.subroutines.directory_routine(process)

            case "ifconfig" | "nmap" | "ping" | "arp" | "ip" | "traceroute" | "ftp":
                return self.subroutines.network_routine(process)

            case "ps" | "kill" | "killall":
                return self.subroutines.process_routine(process, username)

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
                return self.subroutines.file_ops_routine(process)

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
                return self.subroutines.system_routine(process)

            case _:
                self.logger.info(
                    f"Subroutine for command {process.command} is not implemented yet!"
                )
                return
