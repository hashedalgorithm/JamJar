import ctypes, os, signal
from utils.logger import Logger


class Process(Logger):
    def __init__(
        self,
        pid: int,  # process id
        tty: str | None = None,  # terminal associated with the process
        command: str | None = None,  # simple name of executable command
        cwd: (
            str | None
        ) = None,  # current working directory where the process is initiated
        uid: int | None = None,  # user id
        ppid: int | None = None,  # parent process id
        gid: int | None = None,  # parent gid
    ) -> None:
        super().__init__()
        self.pid = pid
        self.tty = tty if tty is not None else self.get_tty(pid)
        self.command = command if command is not None else self.get_command(pid)
        self.cwd = cwd if cwd is not None else self.get_current_working_directory(pid)
        self.uid = uid if uid is not None else self.get_uid(pid)
        self.ppid = ppid if ppid is not None else self.get_ppid(pid)
        self.gid = gid if gid is not None else self.get_gid(gid)

    def read_file(self, path: str) -> str | None:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.critical(f"Could not find the file: {path}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading file: {path} - {e}")
            return None
        finally:
            f.close()

    def get_tty(self, pid: int) -> str | None:
        try:
            return os.readlink(f"/proc/{pid}/fd/0").replace("/dev/", "")
        except FileNotFoundError:
            self.logger.critical(
                f"Could not find the process - {pid} : tty Extraction Failed"
            )
            return
        except Exception as e:
            self.logger.critical(
                f"Error reading files of process - {pid} : tty Extraction Failed"
            )

    def get_command(self, pid: int) -> str | None:
        try:
            content = self.read_file(f"/proc/{pid}/comm")
            return content.strip()
        except FileNotFoundError:
            self.logger.critical(
                f"Could not find the process - {pid} : command Extraction Failed"
            )
            return
        except Exception as e:
            self.logger.critical(
                f"Error reading files of process - {pid} : command Extraction Failed"
            )

    def get_current_working_directory(self, pid: int) -> str | None:
        try:
            return os.readlink(f"/proc/{pid}/cwd")
        except FileNotFoundError:
            self.logger.critical(
                f"Could not find the process - {pid} : cwd Extraction Failed"
            )
            return
        except Exception as e:
            self.logger.critical(
                f"Error reading files of process - {pid} : cwd Extraction Failed"
            )

    def get_uid(self, pid: int) -> int | None:
        content = self.read_file(f"/proc/{pid}/status")
        if content:
            for line in content.splitlines():
                if line.startswith("Uid:"):
                    return int(line.split()[1])  # Extract the effective UID
        return None

    def get_ppid(self, pid: int) -> int | None:
        content = self.read_file(f"/proc/{pid}/status")
        if content:
            for line in content.splitlines():
                if line.startswith("PPid:"):
                    return int(line.split()[1])  # Extract the PPID
        return None

    def get_full_command(self, pid: int) -> str | None:
        content = self.read_file(f"/proc/{pid}/cmdline")
        if content:
            args = content.split("\x00")
            return " ".join(arg for arg in args if arg)
        return None

    def get_gid(self, pid: int) -> int:

        content = self.read_file(f"/proc/{pid}/status")

        if content:
            for line in content:
                if line.startswith("Gid:"):
                    gid = int(line.split()[1])
                    return gid

            raise ValueError(f"GID not found in status")

        return None


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
            self.wait(pid, True)
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
            if pid not in self.attached_processes:
                raise ProcessLookupError(f"Process with PID {pid} is not being traced.")

            self._resume(pid)
            self.wait(pid, False)

        except ProcessLookupError as e:
            self.logger.critical(f"Failed to resume to PID {pid} - {e}")

        except PermissionError:
            self.logger.fatal(
                f"Insufficient permissions to resume process - {pid} - {e}"
            )
            exit(1)

    def detach(self, pid: int):
        try:
            if pid not in self.attached_processes:
                raise ProcessLookupError(f"Process with PID {pid} is not being traced.")

            self._detach(pid)

            self.logger.info(f"Detached process {pid}!")

        except ProcessLookupError as e:
            self.logger.critical(f"Failed to detach to PID {pid} - {e}")

        except PermissionError:
            self.logger.fatal(
                f"Insufficient permissions to detach process - {pid} - {e}"
            )
            exit(1)

    def kill(self, pid: int):
        try:
            if pid not in self.attached_processes:
                raise ProcessLookupError(f"Process with PID {pid} is not being traced.")

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

    def wait(self, pid: int, status: bool) -> None:
        if pid not in self.attached_processes:
            raise ProcessLookupError(f"Process is not attached! - {pid}")

        os.waitpid(pid, os.WUNTRACED if status else os.WCONTINUED)

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
        os.kill(pid, signal.SIGKILL)

    def _resume(self, pid):

        # Resume the process
        if self.libc.ptrace(self.PTRACE_CONT, pid, 0, 0) != 0:
            raise ProcessLookupError(f"Failed to resume PID {pid}")

        os.kill(pid, signal.SIGCONT)
