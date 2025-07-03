import os

from typing import Literal
from utils.logger import Logger


class Process(Logger):

    def __init__(
        self,
        pid: int,  # process id
        tty: str | None = None,  # terminal associated with the process
        time: str | None = None,  # elapsed CPU utilization time for the process
        command: str | None = None,  # simple name of executable command
        uid: int | None = None,  # user id
        ppid: int | None = None,  # parent process id
        c: int | None = None,  # CPU utilization in percentage
        stime: str | None = None,  # start time of the process
        stat: (
            Literal["R", "S", "D", "Z", "T", "I"] | None
        ) = None,  # process state codes
        sid: (
            int | None
        ) = None,  # session ID, If PID == SID, then this process is a session leader
        cpu: int | None = None,  # %CPU: cpu utilization of the process in "##.#" format
        mem: (
            int | None
        ) = None,  # ratio of the process's resident set size to the physical memory on the machine
        rss: int | None = None,  # resident set size
        vsz: int | None = None,  # virtual memory size
        ucmd: int | None = None,  # long name of executable command
    ) -> None:
        super().__init__()
        self.pid = pid
        self.tty = tty if tty is not None else self.get_tty(pid)
        self.time = time if time is not None else self.get_time(pid)
        self.command = command if command is not None else self.get_command(pid)
        self.uid = uid if uid is not None else self.get_uid(pid)
        self.ppid = ppid if ppid is not None else self.get_ppid(pid)
        self.c = c if c is not None else self.get_cpu_utilization(pid)
        self.stime = stime if stime is not None else self.get_start_time(pid)
        self.stat = stat if stat is not None else self.get_process_state(pid)
        self.sid = sid if sid is not None else self.get_session_id(pid)
        self.cpu = cpu if cpu is not None else self.get_cpu_percentage(pid)
        self.mem = mem if mem is not None else self.get_memory_utilization(pid)
        self.rss = rss if rss is not None else self.get_resident_set_size(pid)
        self.vsz = vsz if vsz is not None else self.get_virtual_memory_size(pid)
        self.ucmd = ucmd if ucmd is not None else self.get_full_command(pid)

    def read_file(self, path: str) -> str | None:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"[!] Could not find the file: {path}")
            return None
        except Exception as e:
            print(f"[!] Error reading file: {path} - {e}")
            return None
        finally:
            f.close()

    def get_tty(self, pid: int) -> str | None:
        try:
            return os.readlink(f"/proc/{pid}/fd/0").replace("/dev/", "")
        except FileNotFoundError:
            print(f"[!] Could not find the process - {pid} : tty Extraction Failed")
            return
        except Exception as e:
            print(f"[!] Error reading files of process - {pid} : tty Extraction Failed")

    def get_command(self, pid: int) -> str | None:
        try:
            return os.readlink(f"/proc/{pid}/cwd")
        except FileNotFoundError:
            print(f"[!] Could not find the process - {pid} : cwd Extraction Failed")
            return
        except Exception as e:
            print(f"[!] Error reading files of process - {pid} : cwd Extraction Failed")

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

    def get_time(self, pid: int) -> str | None:
        content = self.read_file(f"/proc/{pid}/stat")
        if content:
            data = content.split()
            utime = int(data[13])
            stime = int(data[14])
            total_time = utime + stime
            return f"{total_time // 3600:02}:{(total_time % 3600) // 60:02}:{total_time % 60:02}"
        return None

    def get_cpu_utilization(self, pid: int) -> int | None:
        content = self.read_file(f"/proc/{pid}/stat")
        if content:
            data = content.split()
            utime = int(data[13])
            stime = int(data[14])
            return utime + stime
        return None

    def get_start_time(self, pid: int) -> str | None:
        content = self.read_file(f"/proc/{pid}/stat")
        if content:
            data = content.split()
            start_time = int(data[21])
            return f"{start_time // 3600:02}:{(start_time % 3600) // 60:02}:{start_time % 60:02}"
        return None

    def get_process_state(
        self, pid: int
    ) -> Literal["R", "S", "D", "Z", "T", "I"] | None:
        content = self.read_file(f"/proc/{pid}/stat")
        if content:
            data = content.split()
            return data[2]
        return None

    def get_session_id(self, pid: int) -> int | None:
        content = self.read_file(f"/proc/{pid}/stat")
        if content:
            data = content.split()
            return int(data[4])
        return None

    def get_cpu_percentage(self, pid: int) -> float | None:
        total_cpu_content = self.read_file(f"/proc/stat")
        process_content = self.read_file(f"/proc/{pid}/stat")
        if total_cpu_content and process_content:
            total_cpu_time = sum(int(value) for value in total_cpu_content.split()[1:])
            data = process_content.split()
            utime = int(data[13])
            stime = int(data[14])
            process_time = utime + stime
            return (process_time / total_cpu_time) * 100
        return None

    def get_memory_utilization(self, pid: int) -> float | None:
        meminfo_content = self.read_file(f"/proc/meminfo")
        statm_content = self.read_file(f"/proc/{pid}/statm")
        if meminfo_content and statm_content:
            total_memory = int(
                meminfo_content.splitlines()[0].split()[1]
            )  # Total memory in kB
            rss = int(statm_content.split()[1])  # Resident set size in pages
            page_size = os.sysconf("SC_PAGE_SIZE")  # Page size in bytes
            rss_kb = rss * (page_size // 1024)  # Convert to kB
            return (rss_kb / total_memory) * 100
        return None

    def get_resident_set_size(self, pid: int) -> int | None:
        statm_content = self.read_file(f"/proc/{pid}/statm")
        if statm_content:
            rss = int(statm_content.split()[1])  # Resident set size in pages
            page_size = os.sysconf("SC_PAGE_SIZE")  # Page size in bytes
            return rss * page_size  # Return RSS in bytes
        return None

    def get_virtual_memory_size(self, pid: int) -> int | None:
        statm_content = self.read_file(f"/proc/{pid}/statm")
        if statm_content:
            vsz = int(statm_content.split()[0])  # Virtual memory size in pages
            page_size = os.sysconf("SC_PAGE_SIZE")  # Page size in bytes
            return vsz * page_size  # Return VSZ in bytes
        return None
