from commands.base import CommandBase
from models.process_group import ProcessGroup
from commands.flagmap import Flagmap, FlagWithArgument
from utils.parser import ParsedCommand
from models.process import Process
from utils import helper
from utils.parser import ParsedCommand


class PS(CommandBase):
    def __init__(self, processes: list[Process], parsed: ParsedCommand) -> None:
        super().__init__("ps")
        self.processes = processes
        self.parsed = parsed
        
    def run(self, tty, pid) -> str | None:
        raise Exception("PS not implemented yet!")
    
    def ps(self, args, tty, uid):
        output = ""
        process_list = []
        processes = []

    flags = {
        # Simple Process Selection
        "a",
        "-A",
        "-a",
        "-d",
        "--deselect",
        "-e",
        "g",
        "-N",
        "T",
        "r",
        "x"
        # Process selection
        "-C",
        "-G",
        "-g",
        "--Group",
        "--group",
        "p",
        "-p",
        "--pid",
        "--ppid",
        "q",
        "-q",
        "--quick-pid",
        "-s",
        "--sid",
        "t",
        "-t",
        "--tty",
        "U" "-U",
        "-u",
        "--User",
        "--user"
        # Output Format Controllers
        "-c",
        "--context" "-f",
        "-F",
        "--format",
        "j",
        "l",
        "-l",
        "-M",
        "O",
        "-O",
        "o",
        "-o",
        "-P",
        "s",
        "u",
        "v",
        "X",
        "-y" "Z"
        # Output Modifiers
        "c",
        "--cols",
        "--columns",
        "--cumulative",
        "-D",
        "--date-format",
        "e" "f",
        "--forest",
        "h",
        "-H",
        "--headers",
        "k",
        "--lines",
        "n",
        "--no-headers",
        "O",
        "--rows",
        "S",
        "--sort",
        "--signames",
        "w",
        "-w",
        "--width"
        # Threads display
        "H",
        "-L",
        "-m",
        "m",
        "-T",
        # information flags
        "--help",
        "--info",
        "L",
        "-V",
        "V",
        "--version",
    }

    attributes: list[Attribute] = [
        Attribute("addr", "ADDR", True),  # Memory Address
        Attribute("cpu", "%CPU"),  # CPU utilization
        Attribute("mem", "%MEM"),  # Memory utilization
        Attribute("ag_id", "AGID"),  # Autogroup identifier
        Attribute("ag_nice", "AGNI"),  # Autogroup nice value
        Attribute("args", "COMMAND"),  # Command with arguments
        Attribute("blocked", "BLOCKED"),  # Mask of blocked signals
        Attribute("bsdstart", "START"),  # Time the command started
        Attribute("bsdtime", "TIME"),  # Accumulated CPU time
        Attribute("c", "C", True),  # Processor utilization
        Attribute("caught", "CAUGHT"),  # Mask of caught signals
        Attribute("cgname", "CGNAME"),  # Control group name
        Attribute("cgroup", "CGROUP"),  # Control groups
        Attribute("cgroupns", "CGROUPNS"),  # Namespace inode number
        Attribute("class", "CLS"),  # Scheduling class
        Attribute("cmd", "CMD"),  # Command name (alias for args)
        Attribute("comm", "COMMAND"),  # Command name (executable only)
        Attribute("cp", "CP"),  # Per-mill CPU usage
        Attribute("cputime", "TIME"),  # Cumulative CPU time
        Attribute("cputimes", "TIME"),  # Cumulative CPU time in seconds
        Attribute("cuc", "%CUC"),  # CPU utilization (including dead children)
        Attribute("cuu", "%CUU"),  # Extended CPU utilization
        Attribute("docker", "DOCKER"),  # Docker container ID
        Attribute("drs", "DRS"),  # Data resident set size
        Attribute("egid", "EGID"),  # Effective group ID
        Attribute("egroup", "EGROUP"),  # Effective group name
        Attribute("eip", "EIP"),  # Instruction pointer
        Attribute("esp", "ESP"),  # Stack pointer
        Attribute("etime", "ELAPSED"),  # Elapsed time since process started
        Attribute("etimes", "ELAPSED"),  # Elapsed time in seconds
        Attribute("environ", "ENVIRON"),  # Environment variables
        Attribute("euid", "EUID"),  # Effective user ID
        Attribute("euser", "EUSER"),  # Effective user name
        Attribute("exe", "EXE"),  # Path to executable
        Attribute("f", "F", True),  # Flags
        Attribute("fds", "FDS"),  # Total open file descriptors
        Attribute("fgid", "FGID"),  # Filesystem access group ID
        Attribute("fgroup", "FGROUP"),  # Filesystem access group name
        Attribute("flag", "F"),  # Flags (alias for f)
        Attribute("flags", "F"),  # Flags (alias for f)
        Attribute("fname", "COMMAND"),  # First 8 bytes of executable name
        Attribute("fuid", "FUID"),  # Filesystem access user ID
        Attribute("fuser", "FUSER"),  # Filesystem access user name
        Attribute("gid", "GID"),  # Real group ID
        Attribute("group", "GROUP"),  # Real group name
        Attribute("htprv", "HTPRV"),  # Private memory backed by hugetlbfs
        Attribute("htshr", "HTSHR"),  # Shared memory backed by hugetlbfs
        Attribute("ignored", "IGNORED"),  # Mask of ignored signals
        Attribute("ipcns", "IPCNS"),  # Namespace inode number
        Attribute("label", "LABEL"),  # Security label (e.g., SELinux context)
        Attribute("lstart", "STARTED"),  # Time the command started (detailed format)
        Attribute("lsession", "SESSION"),  # Login session identifier
        Attribute("luid", "LUID"),  # Login ID
        Attribute("lwp", "LWP"),  # Lightweight process ID (thread ID)
        Attribute("lxc", "LXC"),  # LXC container name
        Attribute("machine", "MACHINE"),  # Machine name for VM/container processes
        Attribute("maj_flt", "MAJFLT"),  # Major page faults
        Attribute("min_flt", "MINFLT"),  # Minor page faults
        Attribute("mntns", "MNTNS"),  # Namespace inode number
        Attribute("netns", "NETNS"),  # Namespace inode number
        Attribute("ni", "NI", True),  # Nice value
        Attribute("nice", "NI"),  # Nice value (alias for ni)
        Attribute("nlwp", "NLWP"),  # Number of threads in the process
        Attribute("numa", "NUMA"),  # NUMA node associated with the process
        Attribute("nwchan", "WCHAN"),  # Kernel function where the process is sleeping
        Attribute("oom", "OOM"),  # Out of Memory score
        Attribute("oomadj", "OOMADJ"),  # Out of Memory adjustment factor
        Attribute("ouid", "OWNER"),  # Unix user ID of session owner
        Attribute("pcap", "PCAP"),  # Permitted capabilities (hexadecimal bitmask)
        Attribute("pcaps", "PCAPS"),  # Permitted capabilities (string of names)
        Attribute("pcpu", "%CPU"),  # CPU utilization (alias for %cpu)
        Attribute("pending", "PENDING"),  # Mask of pending signals
        Attribute("pgid", "PGID"),  # Process group ID
        Attribute("pgrp", "PGRP"),  # Process group ID (alias for pgid)
        Attribute("pid", "PID", True),  # Process ID
        Attribute("pidns", "PIDNS"),  # Namespace inode number
        Attribute("pmem", "%MEM"),  # Memory utilization (alias for %mem)
        Attribute("policy", "POL"),  # Scheduling class
        Attribute("ppid", "PPID", True),  # Parent process ID
        Attribute("pri", "PRI", True),  # Priority
        Attribute("psr", "PSR"),  # Processor last executed on
        Attribute("pss", "PSS"),  # Proportional share size
        Attribute("rbytes", "RBYTES"),  # Bytes fetched from storage
        Attribute("rchars", "RCHARS"),  # Bytes read from storage
        Attribute("rgid", "RGID"),  # Real group ID
        Attribute("rgroup", "RGROUP"),  # Real group name
        Attribute("rops", "ROPS"),  # Read I/O operations
        Attribute("rss", "RSS"),  # Resident set size (physical memory)
        Attribute("rssize", "RSS"),  # Resident set size (alias for rss)
        Attribute("rsz", "RSZ"),  # Resident set size (alias for rss)
        Attribute("rtprio", "RTPRIO"),  # Realtime priority
        Attribute("ruid", "RUID"),  # Real user ID
        Attribute("ruser", "RUSER"),  # Real user name
        Attribute("s", "S", True),  # Minimal state display
        Attribute("sched", "SCH"),  # Scheduling policy
        Attribute("seat", "SEAT"),  # Hardware device identifier
        Attribute("sess", "SESS"),  # Session ID
        Attribute("sgi_p", "P"),  # Processor currently executing on
        Attribute("sgid", "SGID"),  # Saved group ID
        Attribute("sid", "SID"),  # Session ID (alias for sess)
        Attribute("sig", "PENDING"),  # Mask of pending signals
        Attribute("sigcatch", "CAUGHT"),  # Mask of caught signals
        Attribute("sigignore", "IGNORED"),  # Mask of ignored signals
        Attribute("sigmask", "BLOCKED"),  # Mask of blocked signals
        Attribute("size", "SIZE"),  # Approximate swap space required
        Attribute("slice", "SLICE"),  # Slice unit
        Attribute("spid", "SPID"),  # Lightweight process ID (alias for lwp)
        Attribute("stackp", "STACKP"),  # Address of stack start
        Attribute("start", "STARTED"),  # Time the command started
        Attribute("start_time", "START"),  # Starting time/date of the process
        Attribute("stat", "STAT"),  # Multi-character process state
        Attribute("state", "S"),  # Minimal state display (alias for s)
        Attribute("stime", "STIME"),  # Starting time/date (alias for start_time)
        Attribute("suid", "SUID"),  # Saved user ID
        Attribute("supgid", "SUPGID"),  # Supplementary group IDs
        Attribute("supgrp", "SUPGRP"),  # Supplementary group names
        Attribute("suser", "SUSER"),  # Saved user name
        Attribute("svgid", "SVGID"),  # Saved group ID
        Attribute("svuid", "SVUID"),  # Saved user ID
        Attribute("sz", "SZ", True),  # Size in physical pages
        Attribute("tgid", "TGID"),  # Thread group ID
        Attribute("thcount", "THCNT"),  # Number of kernel threads
        Attribute("tid", "TID"),  # Thread ID
        Attribute("time", "TIME"),  # Cumulative CPU time
        Attribute("timens", "TIMENS"),  # Namespace inode number
        Attribute("times", "TIME"),  # Cumulative CPU time in seconds
        Attribute("tname", "TTY"),  # Controlling terminal
        Attribute("tpgid", "TPGID"),  # Foreground process group ID
        Attribute("trs", "TRS"),  # Text resident set size
        Attribute("tt", "TT"),  # Controlling terminal (alias for tty)
        Attribute("tty", "TT", True),  # Controlling terminal (alias for tt)
        Attribute("ucmd", "CMD"),  # Command name (alias for comm)
        Attribute("ucomm", "COMMAND"),  # Command name (alias for comm)
        Attribute("uid", "UID"),  # User ID
        Attribute("uname", "USER"),  # User name
        Attribute("unit", "UNIT"),  # Unit (systemd support)
        Attribute("user", "USER"),  # User name (alias for uname)
        Attribute("userns", "USERNS"),  # Namespace inode number
        Attribute("uss", "USS"),  # Unique set size
        Attribute("utsns", "UTSNS"),  # Namespace inode number
        Attribute("uunit", "UUNIT"),  # User unit (systemd support)
        Attribute("vsize", "VSZ"),  # Virtual memory size (alias for vsz)
        Attribute("vsz", "VSZ"),  # Virtual memory size
        Attribute("wbytes", "WBYTES"),  # Bytes sent to storage
        Attribute("wcbytes", "WCBYTES"),  # Cancelled write bytes
        Attribute("wchan", "WCHAN", True),  # Kernel function where process is sleeping
        Attribute("wchars", "WCHARS"),  # Bytes written to disk
        Attribute("wops", "WOPS"),  # Write I/O operations
    ]

    def __init__(self, process_group: ProcessGroup, uid: int, parsed: ParsedCommand):
        super().__init__()
        self.process_group = process_group
        self.uid = uid
        self.parsed = parsed

        self.filtered_process: list[Process] = []
        self.check_options()

    def check_options(self) -> None:

        if self.parsed.check_arg_exists("-l") and self.parsed.check_arg_exists("-o"):
            raise ValueError(f"PS: Conflicting format options.")

        if self.parsed.check_arg_exists("-y") and not self.parsed.check_arg_exists(
            "-l"
        ):
            raise ValueError(f"PS: Conflicting format options.")

        return

    def get_default_attributes(self) -> list[str]:
        return ["pid", "tty", "time", "cmd"]

    def generate_header(self, attributes: list[Attribute]) -> str:
        header = ""

        for attribute in attributes:
            header = header + f"{attribute.attribute_header}:<10"

        return header

    def check_attribute(self, target_attribute: str) -> Attribute | None:
        for attribute in self.attributes:
            if target_attribute == attribute.attribute_key:
                return True
        else:
            return False

    def get_default_attributes_long(self) -> list[str]:
        """Returns list of format specifiers"""

        return [
            attribute.attribute_key
            for attribute in self.attributes
            if attribute.default
        ]

    def generate_output(self, processes: list[Process]) -> list[str]:
        """This Generates the output to be injected"""
        output: list[str] = []

        format_specifiers = self.flag_map.o.argument.split(",")

        if format_specifiers.__len__() == 0:
            format_specifiers = (
                self.get_default_attributes_long()
                if self.flag_map.l
                else self.get_default_attributes()
            )

        for format_specifier in format_specifiers:
            if self.check_attribute(format_specifier):
                continue
            else:
                raise ValueError(f"Format Specifier - {format_specifier} is invalid")

        attributes = (
            self.flag_map.o.argument.split(",")
            if self.flag_map.o.argument
            else self.get_default_attributes()
        )
        header = self.generate_header(attributes)

        output.append(header)
        output.append("-" * 40)

        # Add process details
        for process in self.process_group.processes:
            output_line = ""

            for attribute in attributes:
                output_line = output_line + f"{process[attribute.attribute_key]:<10}"

            output.append(output_line)

        return output

    def A(self):
        return self.process_group.processes

    def _a(self):
        for process in self.process_group.processes.values():
            if process.stat.find("s") == -1:
                is_exists = next(
                    (x for x in self.filtered_process if x.pid == process.pid), None
                )

                if not is_exists:
                    self.filtered_process.append(process)

        return self.filtered_process

    def a(self):
        for process in self.process_group.processes.values():
            if process.stat.find("s") == -1:
                is_exists = next(
                    (x for x in self.filtered_process if x.pid == process.pid), None
                )

                if not is_exists:
                    self.filtered_process.append(process)

        return self.filtered_process

    def run(self):

        if self.parsed.check_arg_exists("-A"):
            self.filtered_process = self.process_group.processes

        if self.parsed.check_arg_exists("-a"):
            self._a()

        if self.parsed.check_arg_exists("a"):
            self.a()

        return self.generate_output(self.filtered_process)
