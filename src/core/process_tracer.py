import ctypes, os, signal
from models.process import Process
from utils.logger import Logger


class ProcessTracer(Logger):

    libc = ctypes.CDLL("libc.so.6")
    PTRACE_CONT = 7
    PTRACE_ATTACH = 16
    PTRACE_DETACH = 17

    def __init__(self):
        super().__init__()
        self.attached_processes: dict[str, Process] = {}

    def attach(self, pid: int) -> Process | None:
        try:
            if pid in self.attached_processes:
                self.logger.info(f"Process with PID {pid} is already being traced.")
                return self.attached_processes[pid]

            process = self._attach(pid)
            self.logger.info(f"Attached to process [{pid}]")
            return process

        except ProcessLookupError as e:
            self.logger.critical(f"Failed to attach to PID {pid} - {e}")

        except PermissionError:
            self.logger.fatal(
                f"Insufficient permissions to attach process - {pid} - {e}"
            )
            exit(1)

    def resume(self, pid: int):
        try:
            if pid in self.attached_processes:
                self.logger.info(f"Process with PID {pid} is already being traced.")
                return self.attached_processes[pid]

            self._resume(pid)
            self.logger.info(f"Resumed process {pid}!")

        except ProcessLookupError as e:
            self.logger.critical(f"Failed to resume to PID {pid} - {e}")

        except PermissionError:
            self.logger.fatal(
                f"Insufficient permissions to resume process - {pid} - {e}"
            )
            exit(1)

    def kill(self, pid: int):
        try:
            process = self.get_process(pid)

            # IMPORTANT: To mute SIGNAL messages for the user permanently
            # we have to disable monitoring mode permanently
            # 'echo "export PROMPT_COMMAND='set +m'" >> /home/user/.bashrc && source /home/user/.bashrc'
            # In other words this will suppress "Terminated" being printed on the log

            self._kill(pid)
            self.logger.info(f"Killed process {pid}!")

        except ProcessLookupError as e:
            self.logger.critical(f"Failed to kill process {pid} - {e}")
            return None

        except PermissionError as e:
            self.logger.fatal(f"Insufficient permissions to kill process - {pid} - {e}")
            exit(1)

    def get_process(self, pid: int) -> Process:
        process = self.attached_processes.get(pid)

        if process is None:
            raise ProcessLookupError(f"No process found with PID {pid}.")

        return process

    def _attach(self, pid: int) -> Process:
        # Attach to the process
        if self.libc.ptrace(self.PTRACE_ATTACH, pid, 0, 0) != 0:
            raise ProcessLookupError(f"Failed to attach to PID {pid}")

        # Send SIGSTOP to pause the process
        os.kill(pid, signal.SIGSTOP)

        process = Process(pid)
        self.attached_processes[pid] = process

        return process

    def _detach(self, pid: int):
        # Detach from the process
        if self.libc.ptrace(self.PTRACE_DETACH, pid, 0, 0) != 0:
            raise ProcessLookupError(f"Failed to detach from PID {pid}")

        # Remove the process from the attached list
        del self.attached_processes[pid]

    def _kill(self, pid: int):

        self._detach(pid)

        # Kills the process
        os.kill(pid, signal.SIGSTOP)

    def _resume(self, pid):

        # Resume the process
        if self.libc.ptrace(self.PTRACE_CONT, pid, 0, 0) != 0:
            raise ProcessLookupError(f"Failed to resume PID {pid}")

        os.kill(pid, signal.SIGCONT)
