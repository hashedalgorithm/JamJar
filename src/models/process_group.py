from models.process import Process


class ProcessGroup:
    def __init__(self):
        self.processes: dict[int, Process] = self.create_fake_processes()

    def create_fake_processes(self) -> None:
        fake_process_data: list[Process] = [
            {
                "pid": 1,
                "uid": 0,
                "cmd": "systemd",
                "tty": "?",
                "ppid": 0,
                "stat": "Ss",
                "type": "system",
                "load": "light",
            },
            {
                "pid": 2,
                "uid": 0,
                "cmd": "kthreadd",
                "tty": "?",
                "ppid": 0,
                "stat": "S",
                "type": "kernel",
                "load": "light",
            },
            {
                "pid": 3,
                "uid": 0,
                "cmd": "bash",
                "tty": "tty1",
                "ppid": 1,
                "stat": "Ss",
                "type": "foreground",
                "load": "medium",
            },
            {
                "pid": 4,
                "uid": 0,
                "cmd": "ps",
                "tty": "tty1",
                "ppid": 3,
                "stat": "R+",
                "type": "foreground",
                "load": "light",
            },
            {
                "pid": 5,
                "uid": 0,
                "cmd": "sshd",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "daemon",
                "load": "medium",
            },
            {
                "pid": 6,
                "uid": 0,
                "cmd": "cron",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "daemon",
                "load": "light",
            },
            {
                "pid": 7,
                "uid": 0,
                "cmd": "kworker/0:0",
                "tty": "?",
                "ppid": 2,
                "stat": "I",
                "type": "kernel",
                "load": "light",
            },
            {
                "pid": 8,
                "uid": 1000,
                "cmd": "firefox",
                "tty": "tty2",
                "ppid": 3,
                "stat": "Sl",
                "type": "user",
                "load": "heavy",
            },
            {
                "pid": 9,
                "uid": 1000,
                "cmd": "vim",
                "tty": "tty2",
                "ppid": 3,
                "stat": "S",
                "type": "user",
                "load": "medium",
            },
            {
                "pid": 10,
                "uid": 0,
                "cmd": "apache2",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "daemon",
                "load": "medium",
            },
            {
                "pid": 11,
                "uid": 0,
                "cmd": "mysqld",
                "tty": "?",
                "ppid": 1,
                "stat": "Sl",
                "type": "daemon",
                "load": "heavy",
            },
            {
                "pid": 12,
                "uid": 0,
                "cmd": "rsyslogd",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "daemon",
                "load": "light",
            },
            {
                "pid": 13,
                "uid": 0,
                "cmd": "dbus-daemon",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "system",
                "load": "light",
            },
            {
                "pid": 14,
                "uid": 0,
                "cmd": "NetworkManager",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "system",
                "load": "medium",
            },
            {
                "pid": 15,
                "uid": 0,
                "cmd": "udevd",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "system",
                "load": "light",
            },
            {
                "pid": 16,
                "uid": 1000,
                "cmd": "gnome-shell",
                "tty": "tty2",
                "ppid": 3,
                "stat": "Sl",
                "type": "user",
                "load": "heavy",
            },
            {
                "pid": 17,
                "uid": 1000,
                "cmd": "xorg",
                "tty": "tty2",
                "ppid": 3,
                "stat": "Sl",
                "type": "user",
                "load": "heavy",
            },
            {
                "pid": 18,
                "uid": 0,
                "cmd": "kworker/0:1",
                "tty": "?",
                "ppid": 2,
                "stat": "I",
                "type": "kernel",
                "load": "light",
            },
            {
                "pid": 19,
                "uid": 0,
                "cmd": "ksoftirqd/0",
                "tty": "?",
                "ppid": 2,
                "stat": "I",
                "type": "kernel",
                "load": "light",
            },
            {
                "pid": 20,
                "uid": 0,
                "cmd": "irqbalance",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "system",
                "load": "light",
            },
            {
                "pid": 21,
                "uid": 1000,
                "cmd": "spotify",
                "tty": "tty2",
                "ppid": 3,
                "stat": "Sl",
                "type": "user",
                "load": "heavy",
            },
            {
                "pid": 22,
                "uid": 1000,
                "cmd": "gcc",
                "tty": "tty2",
                "ppid": 3,
                "stat": "R",
                "type": "user",
                "load": "medium",
            },
            {
                "pid": 23,
                "uid": 0,
                "cmd": "cupsd",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "daemon",
                "load": "light",
            },
            {
                "pid": 24,
                "uid": 0,
                "cmd": "postfix",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "daemon",
                "load": "medium",
            },
            {
                "pid": 25,
                "uid": 1000,
                "cmd": "python3",
                "tty": "tty2",
                "ppid": 3,
                "stat": "R",
                "type": "user",
                "load": "medium",
            },
            {
                "pid": 26,
                "uid": 0,
                "cmd": "kworker/u2:0",
                "tty": "?",
                "ppid": 2,
                "stat": "I",
                "type": "kernel",
                "load": "light",
            },
            {
                "pid": 27,
                "uid": 0,
                "cmd": "modprobe",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "system",
                "load": "light",
            },
            {
                "pid": 28,
                "uid": 1000,
                "cmd": "htop",
                "tty": "tty2",
                "ppid": 3,
                "stat": "R",
                "type": "user",
                "load": "medium",
            },
            {
                "pid": 29,
                "uid": 0,
                "cmd": "kworker/1:0",
                "tty": "?",
                "ppid": 2,
                "stat": "I",
                "type": "kernel",
                "load": "light",
            },
            {
                "pid": 30,
                "uid": 0,
                "cmd": "journalctl",
                "tty": "?",
                "ppid": 1,
                "stat": "Ss",
                "type": "system",
                "load": "medium",
            },
        ]

        for process in fake_process_data:
            self.add_process(
                Process(
                    pid=process.pid,
                    uid=process.uid,
                    cmd=process.cmd,
                    tty=process.tt,
                    ppid=process.ppid,
                    stat=process.stat,
                    type=process.type,
                    load=process.load,
                )
            )

    def add_process(self, process: Process) -> None:
        """Add a new process to the process group."""
        if process.pid in self.processes:
            raise ValueError(f"Process with PID {process.pid} already exists.")
        self.processes[process.pid] = process

    def delete_process(self, pid: int) -> None:
        """Delete a process from the process group by its PID."""
        if pid not in self.processes:
            raise KeyError(f"Process with PID {pid} does not exist.")
        del self.processes[pid]

    def update_process(self, pid: int, **kwargs) -> None:
        """Update attributes of a process in the process group."""
        if pid not in self.processes:
            raise KeyError(f"Process with PID {pid} does not exist.")
        process = self.processes[pid]
        for key, value in kwargs.items():
            if hasattr(process, key):
                setattr(process, key, value)
            else:
                raise AttributeError(f"Process has no attribute '{key}'.")
