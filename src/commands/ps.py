from commands.base import CommandBase
from models.process_group import ProcessGroup
from .flagmap import Flagmap, FlagWithArgument
from utils.parser import Parser
from models.process import Process


class PSFlagMap(Flagmap):

    def __init__(
        self,
        A: bool = False,  # show all processes
        a: bool = False,  # show processes for all users
        c: bool = False,  # display scheduler information
        d: bool = False,  # display processes except session leaders
        e: bool = False,  # display all processes
        f: bool = False,  # display full-format listing
        l: bool = False,  # display long format
        x: bool = False,  # include processes without a controlling terminal
        forest: bool = False,  # show processes in a forest view
        help: bool = False,  # display help information
        version: bool = False,  # display version information
        no_header: bool = False,  # hides header in long format
        u: FlagWithArgument = FlagWithArgument(
            "u", None
        ),  # display user-oriented format
        p: FlagWithArgument = FlagWithArgument("p", None),  # display process by PID
        t: FlagWithArgument = FlagWithArgument(
            "t", None
        ),  # display processes associated with a terminal
        sort: FlagWithArgument = FlagWithArgument(
            "sort", None
        ),  # sort processes by a specific field
        o: FlagWithArgument = FlagWithArgument("o", None),  # specify output format
        g: FlagWithArgument = FlagWithArgument(
            "g", None
        ),  # display processes for a specific group
        G: FlagWithArgument = FlagWithArgument(
            "G", None
        ),  # display processes for a specific group by name
        U: FlagWithArgument = FlagWithArgument(
            "U", None
        ),  # display processes for a specific real user ID
        C: FlagWithArgument = FlagWithArgument(
            "C", None
        ),  # display processes running a specific command
        cols: FlagWithArgument = FlagWithArgument(
            "cols", None
        ),  # set the width of the output
        rows: FlagWithArgument = FlagWithArgument(
            "rows", None
        ),  # set the height of the output
    ):
        self.a = a
        self.u = u
        self.x = x
        self.f = f
        self.e = e
        self.c = c
        self.A = A
        self.l = l
        self.forest = forest
        self.help = help
        self.version = version
        self.d = d
        self.t = t
        self.p = p
        self.sort = sort
        self.o = o
        self.g = g
        self.G = G
        self.U = U
        self.C = C
        self.cols = cols
        self.rows = rows
        self.no_header = no_header


class Attribute:
    def __init__(
        self, attribute_header: str, attribute_key: str, default: bool = False
    ):
        self.attribute_key = attribute_key
        self.attribute_header = attribute_header
        self.default = default

    def get_attribute_header(self) -> str:
        return self.attribute_header

    def get_attribute_key(self) -> str:
        return self.attribute_key

    def get(self) -> tuple[str, str]:
        return self.attribute_key, self.attribute_header


class PS(CommandBase):

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

    def __init__(self, process_group: ProcessGroup, full_command: str, uid: int):
        super().__init__()
        self.parser
        self.process_group = process_group
        self.uid = uid
        self.flag_map: PSFlagMap = self.initialize_flag_map()

        self.check_options()

    def initialize_flag_map(self, flags: list[str]) -> PSFlagMap:
        """
        Initialize the flag map based on the provided flags.
        """
        flag_map = PSFlagMap()
        for flag in flags:
            if "a" in flag:
                flag_map.a = True
            if "u" in flag:
                flag_map.u = True
            if "x" in flag:
                flag_map.x = True
            if "f" in flag:
                flag_map.f = True
            if "e" in flag:
                flag_map.e = True
            if "c" in flag:
                flag_map.c = True

        return flag_map

    def check_options(self) -> None:

        if self.flag_map.l and self.flag_map.o:
            raise ValueError(f"PS: Conflicting format options.")

        return

    def get_default_attributes(self) -> list[str]:
        return ["pid", "tty", "time", "cmd"]

    def generate_header(self, attributes: list[Attribute]) -> str:
        header = ""

        if self.flag_map.no_header:
            return header

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

    def run(self):
        processes = []

        if self.flag_map.e or self.flag_map.a or self.flag_map.A:
            processes = self.process_group.processes

        # if(self.flag_map.)

        return self.generate_output(processes)
