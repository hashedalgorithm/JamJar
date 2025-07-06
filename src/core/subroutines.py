import os
import time
import errno

from handlers.command_handler import CommandHandler
from core.process_tracer import ProcessTracer
from utils.logger import Logger
from models.process import Process


class Subroutines(Logger):
    def __init__(self, process_tracer: ProcessTracer):
        super().__init__()
        self.command_handler = CommandHandler()
        self.process_tracer = process_tracer

        # Category-based command routing map
        self.command_map = {
            "directory": {"cd", "ls", "rmdir", "mkdir", "mv", "cp", "rm"},
            "network": {"ifconfig", "nmap", "ping", "arp", "ip", "traceroute", "ftp"},
            "process": {"ps", "kill", "killall"},
            "file_ops": {
                "cat", "grep", "echo", "locate", "wget", "curl", "unzip",
                "chmod", "nano", "pico", "vi", "vim", "ln", "crontab"
            },
            "system": {
                "df", "history", "php", "uname", "whoami", "w", "id", "last", "uptime"
            },
        }

    def subroutine_manager(self, process: Process, username: str) -> None:
        command = process.command

        for category, commands in self.command_map.items():
            if command in commands:
                handler = getattr(self, f"{category}_routine", None)
                if handler:
                    return handler(process, username) if category == "process" else handler(process)

        self.logger.warning(f"Subroutine for command '{command}' is not implemented yet.")
        self.release_process(process.pid)

    def release_process(self, pid: int) -> None:
        self.process_tracer.resume(pid)
        self.process_tracer.detach(pid)

    def directory_routine(self, process: Process) -> None:
        self._handle_generic(process, self.command_handler.invoke_directory_handler)

    def network_routine(self, process: Process) -> None:
        output = self.command_handler.invoke_directory_handler(
            process.command, process.get_full_command(process.pid)
        )
        output = self.sanitize_string(output)

        # Special handling for ping
        if isinstance(output, list):
            for i, line in enumerate(output):
                self.inject_output_to_proc(line + "\n", process.ppid)
                if i < 5:
                    time.sleep(1)
        else:
            self.inject_output(process.pid, process.ppid, output, True)

    def process_routine(self, process: Process, username: str) -> None:
        output = self.command_handler.invoke_process_handler(
            process.command, process.get_full_command(process.pid),
            process.tty, username
        )
        output = self.sanitize_string(output)
        self.inject_output(process.pid, process.ppid, output, False)

    def file_ops_routine(self, process: Process) -> None:
        self._handle_generic(process, self.command_handler.invoke_file_ops_handler)

    def system_routine(self, process: Process) -> None:
        self._handle_generic(process, self.command_handler.invoke_system_handler)

    def _handle_generic(self, process: Process, handler_fn) -> None:
        try:
            full_command = process.get_full_command(process.pid)
            output = handler_fn(process.command, full_command)
            output = self.sanitize_string(output)
            self.inject_output(process.pid, process.ppid, output, False)
        except Exception as e:
            self.logger.error(f"Error in handler for command {process.command}: {e}")
            self.release_process(process.pid)

    def sanitize_string(self, message: str) -> str:
        if message and not message.endswith("\n"):
            return message + "\n"
        return message

    def inject_output_to_proc(self, message: str, pid: int) -> None:
        if not message:
            self.logger.info(f"No message to inject to process - {pid}.")
            return

        fd_path = f"/proc/{pid}/fd/1"
        try:
            if not os.path.exists(fd_path):
                raise FileNotFoundError()

            with open(fd_path, "w") as fd:
                fd.write(message)

        except FileNotFoundError:
            print(f"[!] Cannot open {fd_path} — process might have exited.")
        except OSError as e:
            if e.errno == errno.EFAULT:
                print(f"[!] Kernel EFAULT writing to {fd_path}")
            else:
                raise Exception(f"Error injecting output : {e}")

    def inject_output(self, pid: int, ppid: int, message: str, usePID: bool) -> None:
        if message:
            self.inject_output_to_proc(message, pid if usePID else ppid)
        else:
            self.logger.info(f"No output found to inject for pid - {pid}")

        self.logger.info(f"Killing process {pid} after writing message.")
        self.process_tracer.kill(pid)
