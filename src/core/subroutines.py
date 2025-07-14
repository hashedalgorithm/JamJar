import os
import time
import errno
import traceback

from handlers.command_handler import CommandHandler
from core.process_tracer import ProcessTracer, Process
from utils.logger import Logger


class Subroutines(Logger):

    def __init__(self, process_tracer: ProcessTracer):
        super().__init__()
        self.command_handler = CommandHandler()
        self.process_tracer = process_tracer

    def subroutine_manager(self, process: Process, username: str) -> None:
        match process.command:
            case "cd" | "ls" | "rmdir" | "mkdir" | "mv" | "cp" | "rm":
                return self.directory_routine(process)

            case "ifconfig" | "nmap" | "ping" | "arp" | "ip" | "traceroute" | "ftp":
                return self.network_routine(process)

            case "ps" | "kill" | "killall":
                return self.process_routine(process, username)

            case (
                "cat"
                | "grep"
                | "echo"
                | "unzip"
                | "chmod"
                | "nano"
                | "vi"
                | "ln"
                | "crontab"
                | "touch"
            ):
                return self.file_ops_routine(process)

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
                return self.system_routine(process)

            case _:
                self.logger.warning(
                    f"Subroutine for command {process.command} is not implemented yet!"
                )
                self.release_process(process.pid)
                return

    def release_process(self, pid) -> None:
        self.process_tracer.resume(pid)
        self.process_tracer.detach(pid)

    def sync_terminals(self, process: Process) -> None:
        id = process.tty.split("/")[-1]
        self.command_handler.sync_virtual_system(id=id, uid=process.uid)

    def directory_routine(self, process: Process) -> None:
        try:
            self.sync_terminals(process)
            full_command = process.get_full_command(process.pid)
            raw_output = self.command_handler.invoke_directory_handler(
                process.command, full_command, process.cwd
            )
            output = self.sanitize_string(raw_output)
            self.inject_output(process.pid, process.ppid, output, False)

        except Exception as e:
            self.logger.error(
                f"Error in Directory Handler: {e}\n{traceback.format_exc()}"
            )
            self.release_process(process.pid)

    def network_routine(self, process: Process) -> None:
        try:
            self.sync_terminals(process)
            full_command = process.get_full_command(process.pid)
            raw_output = self.command_handler.invoke_directory_handler(
                process.command, full_command
            )
            output = self.sanitize_string(raw_output)

            if isinstance(output, list):  # Special case: ping or similar
                for n, item in enumerate(output):
                    self.inject_output_to_proc(item + "\n", process.ppid)
                    if n < 5:
                        time.sleep(1)
            else:
                self.inject_output(process.pid, process.ppid, output, True)

        except Exception as e:
            self.logger.error(
                f"Error in Network Handler: {e}\n{traceback.format_exc()}"
            )
            self.release_process(process.pid)

    def process_routine(self, process: Process, username: str) -> None:
        try:
            self.sync_terminals(process)
            full_command = process.get_full_command(process.pid)
            raw_output = self.command_handler.invoke_process_handler(
                process.command, full_command, process.tty, username
            )
            output = self.sanitize_string(raw_output)
            self.inject_output(process.pid, process.ppid, output, False)

        except Exception as e:
            self.logger.error(
                f"Error in Process Handler: {e}\n{traceback.format_exc()}"
            )
            self.release_process(process.pid)

    def system_routine(self, process: Process) -> None:
        try:
            self.sync_terminals(process)
            full_command = process.get_full_command(process.pid)
            raw_output = self.command_handler.invoke_system_handler(
                process.command, full_command
            )
            output = self.sanitize_string(raw_output)
            self.inject_output(process.pid, process.ppid, output, False)

        except Exception as e:
            self.logger.error(f"Error in System Handler: {e}\n{traceback.format_exc()}")
            self.release_process(process.pid)

    def file_ops_routine(self, process: Process) -> None:
        try:
            self.sync_terminals(process)
            full_command = process.get_full_command(process.pid)
            raw_output = self.command_handler.invoke_file_ops_handler(
                process.command, full_command
            )
            output = self.sanitize_string(raw_output)
            self.inject_output(process.pid, process.ppid, output, False)

        except Exception as e:
            self.logger.error(
                f"Error in File Operations Handler: {e}\n{traceback.format_exc()}"
            )
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
            self.logger.error(f"Cannot open {fd_path} — process might have exited.")
        except OSError as e:
            if e.errno == errno.EFAULT:
                self.logger.critical(f"Kernel EFAULT writing to {fd_path}")
            else:
                raise Exception(
                    f"Error injecting output : {e} \n{traceback.format_exc()}"
                )
        finally:
            fd.close()

    def inject_output(self, pid: int, ppid: int, message: str, usePID: bool) -> None:
        if message:
            self.inject_output_to_proc(message, pid if usePID else ppid)
        else:
            self.logger.info(f"No output found to inject for pid - {pid}")

        self.logger.info(f"Killing process {pid} after writing message.")
        self.process_tracer.kill(pid)
