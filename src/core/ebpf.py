import os
import datetime

from bcc import BPF
from collections import defaultdict
from utils.helper import get_username_by_uid
from core.process_tracer import ProcessTracer
from core.subroutines import Subroutines


class EventType:
    EVENT_ARG = 0
    EVENT_RET = 1


class EBPF:

    def __init__(self, ebpf_path: str):
        self.process_tracer = ProcessTracer()
        self.argv = defaultdict(list)
        self.bpf = BPF(text=self.load_bpf_c_code(ebpf_path))
        self.subroutines = Subroutines(self.process_tracer)

        execve_fnname = self.bpf.get_syscall_fnname("execve")
        self.bpf.attach_kprobe(event=execve_fnname, fn_name="syscall__execve")
        self.bpf.attach_kretprobe(event=execve_fnname, fn_name="do_ret_sys_execve")

    def load_bpf_c_code(self, ebpf_path: str) -> str:
        try:
            with open(ebpf_path, "r") as f:
                bpf_source = f.read()
                return bpf_source
        except FileNotFoundError:
            print(f"[!] Could not find eBPF source file at {ebpf_path}.")
            exit(1)

    def proc_event(self, cpu: int, data: int, size: int) -> None:

        event = self.bpf["events"].event(data)

        if event.type == EventType.EVENT_ARG:
            print("[+] EVENT ARG", event.pid, event.argv, event)
            self.argv[event.pid].append(event.argv)
        elif event.type == EventType.EVENT_RET:
            print("[+] EVENT RET", event.pid, event.argv, event)

            if event.pid not in self.argv:
                print(f"[!] No event found for PID {event.pid}.")
                return

            # process = self.process_tracer.attach(event.pid)
            argv_text = b" ".join(self.argv[event.pid]).replace(b"\n", b"\\n")

            try:
                cwd = os.readlink(f"/proc/{event.pid}/cwd")
                tty = os.readlink(f"/proc/{event.pid}/fd/0").replace("/dev/", "")
                username = get_username_by_uid(event.uid)
                # Getting cleaned command
                print("[-] DEBUGGING ", event.pid, event.comm, argv_text)
                full_command, cmd_wo_args = self.cleanup_cmd(event.comm, argv_text)

                # Print event to console
                self.print_event(full_command, cwd, event.uid)
                # Handle commands
                # self.event_handler(
                #     cmd_wo_args,
                #     event.pid,
                #     full_command,
                #     cwd,
                #     tty,
                #     event.ppid,
                #     username,
                # )
                print(
                    "[+] DEBUGGING: argv contents:",
                    self.argv[event.pid],
                    full_command,
                    cmd_wo_args,
                )
                del self.argv[event.pid]
                print(f"[+] Cleared argv for PID {event.pid}")
            except FileNotFoundError:
                print(f"[!] Process {event.pid} exited before we could inspect /proc")
            except Exception as e:
                print(f"[!] Error processing event for PID {event.pid}: {e}")
                return

    def event_handler(
        self,
        comm: str,
        pid: int,
        full_cmd: str,
        cwd: str,
        tty: str,
        ppid: int,
        username: str,
    ) -> None:
        match comm:
            case "ls" | "rm" | "touch":
                return self.subroutines.dir_routine(pid, ppid, full_cmd, cwd)

            case "ping" | "arp" | "ip" | "traceroute":
                return self.subroutines.network_routine(pid, ppid, full_cmd)

            case "ps" | "kill" | "killall":
                return self.subroutines.process_routine(
                    pid, ppid, full_cmd, tty, username
                )
            case _:
                print(f"[!] Subroutine for command {comm} is not implemented yet!")
                return

    # Cleanup Commands
    def cleanup_cmd(self, command: str, args: str) -> tuple[str, str]:
        cmd = command.replace(b"/usr/bin/%s " % (command), b"%s" % (command)).replace(
            b"/usr/sbin/%s " % (command), b"%s" % (command)
        )
        arguments = (
            args.replace(b" --color=auto", b"")
            .replace(b"/usr/bin/%s" % (command), b"")
            .replace(b"/usr/sbin/%s" % (command), b"")
        )
        fullcmd = cmd + arguments
        return fullcmd.decode(), cmd.decode()

    # Print Trace and Kill Events to console
    def print_event(self, command: str, cwd: str, uid: int) -> None:
        ct = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(f"[+][{ct}] Traced Command: [{command}]")
        print(f"\t\\--> Executed in [{cwd}] by UID [{uid}]")

    def quit_debugger(self):
        return self.process_tracer.debugger.quit()
