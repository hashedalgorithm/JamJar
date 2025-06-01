import os
import time
import errno

from handlers.command_handler import CommandHandler
from ptrace.debugger import PtraceProcess
from core.process_tracer import ProcessTracer


class Subroutines:

    def __init__(self, process_tracer: ProcessTracer):
        self.command_handler = CommandHandler()
        self.process_tracer = process_tracer

    def check_linebreak(self, message: str) -> str:
        if not message == None and not message.endswith("\n") and not message == "":
            return message + "\n"
        return message

    def write_to_proc(self, message: str, pid: int) -> None:
        if not message:
            print("[!] No message to write to process.")
            return

        # Set path for the process to write to
        fd_path = f"/proc/{pid}/fd/1"
        try:
            # Open file descriptor for writing
            if not os.path.exists(fd_path):
                print(f"[!] FD path {fd_path} doesn't exist.")
                return

            with open(fd_path, "w") as fd:
                fd.write(message)
        except FileNotFoundError:
            print(f"[!] Cannot open {fd_path} — process might have exited.")
        except OSError as e:
            if e.errno == errno.EFAULT:
                print(f"[!] Kernel EFAULT writing to {fd_path}")
            else:
                print(f"[!] OSError {e.errno}: {e}")

    def dir_routine(
        self,
        pid: int,
        ppid: int,
        command: str,
        cwd: str,
    ) -> None:
        cmd_output = self.check_linebreak(
            self.command_handler.invoke_dir(command, src_dir=cwd)
        )
        self.safe_write_then_kill(pid, ppid, cmd_output, False)

    def network_routine(self, pid: int, ppid: int, command: str) -> None:
        cmd_output = self.command_handler.invoke_network(command)
        # Special case ping
        if type(cmd_output) == list:
            for n, item in enumerate(cmd_output):
                self.write_to_proc(item + "\n", str(ppid))
                if n < 5:
                    time.sleep(1)
        # Write modified output to target process
        else:
            self.safe_write_then_kill(
                str(pid), ppid, self.check_linebreak(cmd_output), True
            )

    def process_routine(
        self,
        pid: int,
        ppid: int,
        command: str,
        tty: str,
        uname: str,
    ) -> None:
        cmd_output = self.check_linebreak(
            self.command_handler.invoke_process(command, tty, uname)
        )
        # Write modified output to target process

        self.safe_write_then_kill(pid, ppid, self.check_linebreak(cmd_output), False)

    def safe_write_then_kill(self, pid: int, ppid: int, message: str, usePID: bool):
        try:
            if message:
                self.write_to_proc(
                    self.check_linebreak(message), pid if usePID else ppid
                )
        finally:
            print(f"[+] Killing process {pid} after writing message.")
            self.process_tracer.kill(pid)
