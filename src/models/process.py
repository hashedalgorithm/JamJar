import os, random, string
from typing import Literal, Optional, Dict
from datetime import datetime, timedelta

ProcessType = Literal[
    "system",
    "user",
    "daemon",
    "interactive",
    "batch",
    "real-time",
    "zombie",
    "orphan",
    "kernal",
    "foreground",
    "background",
]
ProcessFlag = Literal[0, 1, 4]
ProcessLoad = Literal["light", "medium", "heavy"]


class Process:
    def __init__(
        self,
        pid: int,  # Process ID
        type: ProcessType,
        load: ProcessLoad = "medium",
        tty: Optional[str] = "?",  # Controlling terminal
        time: Optional[str] = None,  # Cumulative CPU time
        f: ProcessFlag = 0,  # Process flags (0: no special flag, 1: system process, 4: user process)
        addr: Optional[str] = "-",  # Memory address
        cpu: Optional[float] = None,  # CPU utilization (%CPU)
        mem: Optional[float] = None,  # Memory utilization (%MEM)
        ag_id: Optional[int] = None,  # Autogroup identifier
        ag_nice: Optional[int] = None,  # Autogroup nice value
        args: Optional[str] = None,  # Command with arguments
        blocked: Optional[str] = None,  # Mask of blocked signals
        bsdstart: Optional[str] = None,  # Time the command started
        bsdtime: Optional[str] = None,  # Accumulated CPU time
        c: Optional[int] = None,  # Processor utilization
        caught: Optional[str] = None,  # Mask of caught signals
        cgname: Optional[str] = None,  # Control group name
        cgroup: Optional[str] = None,  # Control groups
        cgroupns: Optional[int] = None,  # Namespace inode number
        cls: Optional[str] = None,  # Scheduling class
        cmd: Optional[str] = None,  # Command name (alias for args)
        comm: Optional[str] = None,  # Command name (executable only)
        cp: Optional[float] = None,  # Per-mill CPU usage
        cputime: Optional[str] = None,  # Cumulative CPU time
        cputimes: Optional[int] = None,  # Cumulative CPU time in seconds
        cuc: Optional[float] = None,  # CPU utilization (including dead children)
        cuu: Optional[float] = None,  # Extended CPU utilization
        docker: Optional[str] = None,  # Docker container ID
        drs: Optional[int] = None,  # Data resident set size
        egid: Optional[int] = None,  # Effective group ID
        egroup: Optional[str] = None,  # Effective group name
        eip: Optional[str] = None,  # Instruction pointer
        esp: Optional[str] = None,  # Stack pointer
        etime: Optional[str] = None,  # Elapsed time since process started
        etimes: Optional[int] = None,  # Elapsed time in seconds
        environ: Optional[Dict[str, str]] = None,  # Environment variables
        euid: Optional[int] = None,  # Effective user ID
        euser: Optional[str] = None,  # Effective user name
        exe: Optional[str] = None,  # Path to executable
        fds: Optional[int] = None,  # Total open file descriptors
        fgid: Optional[int] = None,  # Filesystem access group ID
        fgroup: Optional[str] = None,  # Filesystem access group name
        fname: Optional[str] = None,  # First 8 bytes of executable name
        fuid: Optional[int] = None,  # Filesystem access user ID
        fuser: Optional[str] = None,  # Filesystem access user name
        gid: Optional[int] = None,  # Real group ID
        group: Optional[str] = None,  # Real group name
        htprv: Optional[int] = None,  # Private memory backed by hugetlbfs
        htshr: Optional[int] = None,  # Shared memory backed by hugetlbfs
        ignored: Optional[str] = None,  # Mask of ignored signals
        ipcns: Optional[int] = None,  # Namespace inode number
        label: Optional[str] = None,  # Security label (e.g., SELinux context)
        lstart: Optional[str] = None,  # Time the command started (detailed format)
        lsession: Optional[int] = None,  # Login session identifier
        luid: Optional[int] = None,  # Login ID
        lwp: Optional[int] = None,  # Lightweight process ID (thread ID)
        lxc: Optional[str] = None,  # LXC container name
        machine: Optional[str] = None,  # Machine name for VM/container processes
        maj_flt: Optional[int] = None,  # Major page faults
        min_flt: Optional[int] = None,  # Minor page faults
        mntns: Optional[int] = None,  # Namespace inode number
        netns: Optional[int] = None,  # Namespace inode number
        ni: int = 0,  # Nice value (-20 to 19, default is 0)
        nlwp: Optional[int] = None,  # Number of threads in the process
        numa: Optional[int] = None,  # NUMA node associated with the process
        nwchan: Optional[str] = None,  # Kernel function where the process is sleeping
        oom: Optional[int] = None,  # Out of Memory score
        oomadj: Optional[int] = None,  # Out of Memory adjustment factor
        ouid: Optional[int] = None,  # Unix user ID of session owner
        pcap: Optional[str] = None,  # Permitted capabilities (hexadecimal bitmask)
        pcaps: Optional[str] = None,  # Permitted capabilities (string of names)
        pcpu: Optional[float] = None,  # CPU utilization (alias for %cpu)
        pending: Optional[str] = None,  # Mask of pending signals
        pgid: Optional[int] = None,  # Process group ID
        pgrp: Optional[int] = None,  # Process group ID (alias for pgid)
        pidns: Optional[int] = None,  # Namespace inode number
        pmem: Optional[float] = None,  # Memory utilization (alias for %mem)
        policy: Optional[str] = None,  # Scheduling class
        ppid: Optional[int] = None,  # Parent process ID
        pri: int = 80,  # Priority of the process (default is 80)
        psr: Optional[int] = None,  # Processor last executed on
        pss: Optional[int] = None,  # Proportional share size
        rbytes: Optional[int] = None,  # Bytes fetched from storage
        rchars: Optional[int] = None,  # Bytes read from storage
        rgid: Optional[int] = None,  # Real group ID
        rgroup: Optional[str] = None,  # Real group name
        rops: Optional[int] = None,  # Read I/O operations
        rss: Optional[int] = None,  # Resident set size (physical memory)
        rssize: Optional[int] = None,  # Resident set size (alias for rss)
        rsz: Optional[int] = None,  # Resident set size (alias for rss)
        rtprio: Optional[int] = None,  # Realtime priority
        ruid: Optional[int] = None,  # Real user ID
        ruser: Optional[str] = None,  # Real user name
        s: Optional[str] = None,  # Minimal state display
        sched: Optional[str] = None,  # Scheduling policy
        seat: Optional[str] = None,  # Hardware device identifier
        sess: Optional[int] = None,  # Session ID
        sgi_p: Optional[int] = None,  # Processor currently executing on
        sgid: Optional[int] = None,  # Saved group ID
        sid: Optional[int] = None,  # Session ID (alias for sess)
        sig: Optional[str] = None,  # Mask of pending signals
        sigcatch: Optional[str] = None,  # Mask of caught signals
        sigignore: Optional[str] = None,  # Mask of ignored signals
        sigmask: Optional[str] = None,  # Mask of blocked signals
        size: Optional[int] = None,  # Approximate swap space required
        slice: Optional[str] = None,  # Slice unit
        spid: Optional[int] = None,  # Lightweight process ID (alias for lwp)
        stackp: Optional[str] = None,  # Address of stack start
        start: Optional[str] = None,  # Time the command started
        start_time: Optional[str] = None,  # Starting time/date of the process
        stat: Optional[str] = None,  # Multi-character process state
        state: Optional[str] = None,  # Minimal state display (alias for s)
        stime: Optional[str] = None,  # Starting time/date (alias for start_time)
        suid: Optional[int] = None,  # Saved user ID
        supgid: Optional[str] = None,  # Supplementary group IDs
        supgrp: Optional[str] = None,  # Supplementary group names
        suser: Optional[str] = None,  # Saved user name
        svgid: Optional[int] = None,  # Saved group ID
        svuid: Optional[int] = None,  # Saved user ID
        sz: Optional[int] = None,  # Size in physical pages
        tgid: Optional[int] = None,  # Thread group ID
        thcount: Optional[int] = None,  # Number of kernel threads
        tid: Optional[int] = None,  # Thread ID
        timens: Optional[int] = None,  # Namespace inode number
        times: Optional[int] = None,  # Cumulative CPU time in seconds
        tname: Optional[str] = None,  # Controlling terminal
        tpgid: Optional[int] = None,  # Foreground process group ID
        trs: Optional[int] = None,  # Text resident set size
        tt: Optional[str] = None,  # Controlling terminal (alias for tty)
        ucmd: Optional[str] = None,  # Command name (alias for comm)
        ucomm: Optional[str] = None,  # Command name (alias for comm)
        uid: Optional[int] = None,  # User ID
        uname: Optional[str] = None,  # User name
        unit: Optional[str] = None,  # Unit (systemd support)
        user: Optional[str] = None,  # User name (alias for uname)
        userns: Optional[int] = None,  # Namespace inode number
        uss: Optional[int] = None,  # Unique set size
        utsns: Optional[int] = None,  # Namespace inode number
        uunit: Optional[str] = None,  # User unit (systemd support)
        vsize: Optional[int] = None,  # Virtual memory size (alias for vsz)
        vsz: Optional[int] = None,  # Virtual memory size
        wbytes: Optional[int] = None,  # Bytes sent to storage
        wcbytes: Optional[int] = None,  # Cancelled write bytes
        wchan: Optional[str] = None,  # Kernel function where process is sleeping
        wchars: Optional[int] = None,  # Bytes written to disk
        wops: Optional[int] = None,  # Write I/O operations
    ):
        self.type = type
        self.load = load
        # System process attributes
        self.pid = pid
        self.mem = mem if mem is not None else self.generate_memory_utilization()
        self.addr = addr if addr is not None else self.generate_addr()
        self.ag_id = ag_id if ag_id is not None else self.generate_ag_id()
        self.ag_nice = ag_nice if ag_nice is not None else self.generate_ag_nice()
        self.args = args if args is not None else self.generate_args()
        self.blocked = blocked if blocked is not None else self.generate_blocked()
        self.bsdstart = bsdstart if bsdstart is not None else self.generate_bsdstart()
        self.bsdtime = bsdtime if bsdtime is not None else self.generate_bsdtime()
        self.c = c if c is not None else self.generate_c()
        self.caught = caught if caught is not None else self.generate_caught()
        self.cgname = cgname if cgname is not None else self.generate_cgname()
        self.cgroup = cgroup if cgroup is not None else self.generate_cgroup()
        self.cgroupns = cgroupns if cgroupns is not None else self.generate_cgroupns()
        self.cls = cls if cls is not None else self.generate_class()
        self.cmd = cmd if cmd is not None else self.generate_comm()
        self.comm = comm if comm is not None else self.generate_comm()
        self.cp = cp if cp is not None else self.generate_cp()
        self.cputime = cputime if cputime is not None else self.generate_cputime()
        self.cputimes = cputimes if cputimes is not None else self.generate_cputimes()
        self.cuc = cuc if cuc is not None else self.generate_cuc()
        self.cuu = cuu if cuu is not None else self.generate_cuu()
        self.docker = docker if docker is not None else self.generate_docker()
        self.drs = drs if drs is not None else self.generate_drs()
        self.egid = egid if egid is not None else self.generate_egid()
        self.egroup = egroup if egroup is not None else self.generate_egroup()
        self.eip = eip if eip is not None else self.generate_eip()
        self.esp = esp if esp is not None else self.generate_esp()
        self.etime = etime if etime is not None else self.generate_etime()
        self.etimes = etimes if etimes is not None else self.generate_etimes()
        self.environ = environ if environ is not None else self.generate_env()
        self.euid = euid if euid is not None else self.generate_euid()
        self.euser = euser if euser is not None else self.generate_euser()
        self.exe = exe if exe is not None else self.generate_exe()
        self.f = f if f is not None else self.generate_f()
        self.fds = fds if fds is not None else self.generate_fds()
        self.fgid = fgid if fgid is not None else self.generate_fgid()
        self.fgroup = fgroup if fgroup is not None else self.generate_fgroup()
        self.fname = fname if fname is not None else self.generate_fname()
        self.fuid = fuid if fuid is not None else self.generate_fuid()
        self.fuser = fuser if fuser is not None else self.generate_fuser()
        self.gid = gid if gid is not None else self.generate_gid()
        self.group = group if group is not None else self.generate_group()
        self.htprv = htprv if htprv is not None else self.generate_htprv()
        self.htshr = htshr if htshr is not None else self.generate_htshr()
        self.ignored = ignored if ignored is not None else self.generate_ignored()
        self.ipcns = ipcns if ipcns is not None else self.generate_ipcns()
        self.label = label if label is not None else self.generate_label()
        self.lstart = lstart if lstart is not None else self.generate_lstart()
        self.lsession = lsession if lsession is not None else self.generate_lsession()
        self.luid = luid if luid is not None else self.generate_luid()
        self.lwp = lwp if lwp is not None else self.generate_lwp()
        self.lxc = lxc if lxc is not None else self.generate_lxc()
        self.machine = machine if machine is not None else self.generate_machine()
        self.maj_flt = maj_flt if maj_flt is not None else self.generate_maj_flt()
        self.min_flt = min_flt if min_flt is not None else self.generate_min_flt()
        self.mntns = mntns if mntns is not None else self.generate_mntns()
        self.netns = netns if netns is not None else self.generate_netns()
        self.ni = ni if ni is not None else self.generate_ni()
        self.nlwp = nlwp if nlwp is not None else self.generate_nlwp()
        self.numa = numa if numa is not None else self.generate_numa()
        self.nwchan = nwchan if nwchan is not None else self.generate_nwchan()
        self.oom = oom if oom is not None else self.generate_oom()
        self.oomadj = oomadj if oomadj is not None else self.generate_oomadj()
        self.ouid = ouid if ouid is not None else self.generate_ouid()
        self.pcap = pcap if pcap is not None else self.generate_pcap()
        self.pcaps = pcaps if pcaps is not None else self.generate_pcaps()
        self.pcpu = pcpu if pcpu is not None else self.generate_pcpu()
        self.pending = pending if pending is not None else self.generate_pending()
        self.pgid = pgid if pgid is not None else self.generate_pgid()
        self.pgrp = pgrp if pgrp is not None else self.generate_pgid()
        self.pidns = pidns if pidns is not None else self.generate_pidns()
        self.pmem = pmem if pmem is not None else self.generate_pmem()
        self.policy = policy if policy is not None else self.generate_policy()
        self.ppid = ppid if ppid is not None else self.generate_ppid()
        self.pri = pri if pri is not None else self.generate_pri()
        self.psr = psr if psr is not None else self.generate_psr()
        self.pss = pss if pss is not None else self.generate_pss()
        self.rbytes = rbytes if rbytes is not None else self.generate_rbytes()
        self.rchars = rchars if rchars is not None else self.generate_rchars()
        self.rgid = rgid if rgid is not None else self.generate_rgid()
        self.rgroup = rgroup if rgroup is not None else self.generate_rgroup()
        self.rops = rops if rops is not None else self.generate_rops()
        self.rss = rss if rss is not None else self.generate_rss()
        self.rssize = rssize if rssize is not None else self.generate_rss()
        self.rsz = rsz if rsz is not None else self.generate_rsz()
        self.rtprio = rtprio if rtprio is not None else self.generate_rtprio()
        self.ruid = ruid if ruid is not None else self.generate_ruid()
        self.ruser = ruser if ruser is not None else self.generate_ruser()
        self.s = s if s is not None else self.generate_s()
        self.sched = sched if sched is not None else self.generate_sched()
        self.seat = seat if seat is not None else self.generate_seat()
        self.sess = sess if sess is not None else self.generate_sess()
        self.sgi_p = sgi_p if sgi_p is not None else self.generate_sgi_p()
        self.sgid = sgid if sgid is not None else self.generate_sgid()
        self.sid = sid if sid is not None else self.generate_sid()
        self.sig = sig if sig is not None else self.generate_sig()
        self.sigcatch = sigcatch if sigcatch is not None else self.generate_sigcatch()
        self.sigignore = (
            sigignore if sigignore is not None else self.generate_sigignore()
        )
        self.sigmask = sigmask if sigmask is not None else self.generate_sigmask()
        self.size = size if size is not None else self.generate_size()
        self.slice = slice if slice is not None else self.generate_slice()
        self.spid = spid if spid is not None else self.generate_spid()
        self.stackp = stackp if stackp is not None else self.generate_stackp()
        self.start = start if start is not None else self.generate_start()
        self.start_time = (
            start_time if start_time is not None else self.generate_start_time()
        )
        self.stat = stat if stat is not None else self.generate_stat()
        self.state = state if state is not None else self.generate_s()
        self.stime = stime if stime is not None else self.generate_stime()
        self.suid = suid if suid is not None else self.generate_suid()
        self.supgid = supgid if supgid is not None else self.generate_supgid()
        self.supgrp = supgrp if supgrp is not None else self.generate_supgrp()
        self.suser = suser if suser is not None else self.generate_suser()
        self.svgid = svgid if svgid is not None else self.generate_svgid()
        self.svuid = svuid if svuid is not None else self.generate_svuid()
        self.sz = sz if sz is not None else self.generate_sz()
        self.tgid = tgid if tgid is not None else self.generate_tgid()
        self.thcount = thcount if thcount is not None else self.generate_thcount()
        self.tid = tid if tid is not None else self.generate_tid()
        self.time = time if time is not None else self.generate_time()
        self.timens = timens if timens is not None else self.generate_timens()
        self.times = times if times is not None else self.generate_times()
        self.tname = tname if tname is not None else self.generate_tname()
        self.tpgid = tpgid if tpgid is not None else self.generate_tpgid()
        self.trs = trs if trs is not None else self.generate_trs()
        self.tt = tt if tt is not None else self.generate_tty()
        self.ucmd = ucmd if ucmd is not None else self.generate_comm()
        self.ucomm = ucomm if ucomm is not None else self.generate_comm()
        self.uid = uid if uid is not None else self.generate_uid()
        self.uname = uname if uname is not None else self.generate_uname()
        self.unit = unit if unit is not None else self.generate_unit()
        self.user = user if user is not None else self.generate_user()
        self.userns = userns if userns is not None else self.generate_userns()
        self.uss = uss if uss is not None else self.generate_uss()
        self.utsns = utsns if utsns is not None else self.generate_utsns()
        self.uunit = uunit if uunit is not None else self.generate_uunit()
        self.vsize = vsize if vsize is not None else self.generate_vsize()
        self.vsz = vsz if vsz is not None else self.generate_vsz()
        self.wbytes = wbytes if wbytes is not None else self.generate_wbytes()
        self.wcbytes = wcbytes if wcbytes is not None else self.generate_wcbytes()
        self.wchan = wchan if wchan is not None else self.generate_wchan()
        self.wchars = wchars if wchars is not None else self.generate_wchars()
        self.wops = wops if wops is not None else self.generate_wops()

    def generate_random_value_based_on_load_round(
        self,
        light: tuple[int | float, int | float],
        medium: tuple[int | float, int | float],
        heavy: tuple[int | float, int | float],
        round: int = 1,
    ):
        # Determine the value range based on load
        if self.load == "light":
            # Light load: Lower value
            return round(random.uniform(light[0], light[1]), round)
        elif self.load == "medium":
            # Medium load: Moderate value
            return round(random.uniform(medium[0], medium[1]), round)
        elif self.load == "heavy":
            # Heavy load: Higher value
            return round(random.uniform(heavy[0], heavy[1]), round)
        else:
            # If load does not affect the value, generate a generic value
            return round(random.uniform(light[0], heavy[1]), round)

    def generate_random_value_by_load(
        self,
        light: tuple[int | float, int | float],
        medium: tuple[int | float, int | float],
        heavy: tuple[int | float, int | float],
    ):
        # Determine the processor utilization range based on load
        if self.load == "light":
            # Light load: Lower CPU utilization
            return random.randint(light[0], light[1])
        elif self.load == "medium":
            # Medium load: Moderate CPU utilization
            return random.randint(medium[0], medium[1])
        elif self.load == "heavy":
            # Heavy load: Higher CPU utilization
            return random.randint(heavy[0], heavy[1])
        else:
            # If load does not affect the value, generate a generic CPU utilization
            return random.randint(light[0], heavy[1])

    def generate_random_value_based_on_type(
        self,
        low: tuple[int | float, int | float],
        mid: tuple[int | float, int | float],
        high: tuple[int | float, int | float],
        range: tuple[int | float, int | float] | None = None,
        low_items: ProcessType = ["system", "kernel"],
        mid_items: ProcessType = ["user", "interactive", "foreground"],
        high_items: ProcessType = ["daemon", "batch", "background"],
    ) -> int:
        fallback_range = range if range is not None else (low[0], high[1])
        if self.type in low_items:
            return random.randint(
                low[0], low[1]
            )  # System/kernel processes may have lower inode numbers
        elif self.type in mid_items:
            return random.randint(
                mid[0], mid[1]
            )  # User processes may have moderate inode numbers
        elif self.type in high_items:
            return random.randint(
                high[0], high[1]
            )  # Daemon processes may have higher inode numbers
        else:
            return random.randint(fallback_range[0], fallback_range[1])  # Default range

    def generate_memory_utilization(self) -> float:
        """
        Generate a random memory utilization percentage for a process.

        Returns:
            float: A randomly generated memory utilization percentage between 0.0 and 100.0.
        """
        return self.generate_random_value_based_on_load_round(
            light=[0.0, 30.0], medium=[30.0, 70.0], heavy=[70.0, 100.0], round=2
        )

    def generate_ag_id(self) -> int:
        """
        Generate a random autogroup identifier for a process.

        Returns:
            int: A randomly generated autogroup identifier.
        """
        return self.generate_random_value_by_load(
            light=[0, 10000], medium=[10000, 30000], heavy=[30000, 65535]
        )

    def generate_ag_nice(self) -> int:
        """
        Generate a random autogroup nice value for a process.

        Returns:
            int: A randomly generated autogroup nice value between -20 and 19.
        """
        # Default range for `ag_nice`
        min_nice = -20
        max_nice = 19

        # Adjust `ag_nice` based on process type
        if self.type == "system":
            # System processes typically have higher priority (lower nice value)
            return random.randint(min_nice, -10)
        elif self.type == "user":
            # User processes have medium priority
            return random.randint(-10, 10)
        elif self.type == "background":
            # Background processes have lower priority (higher nice value)
            return random.randint(10, max_nice)

        # Adjust `ag_nice` based on system load
        if self.load > 80.0:
            # High system load: prioritize critical processes
            return random.randint(min_nice, -5)
        elif self.load < 20.0:
            # Low system load: allow more flexibility for background processes
            return random.randint(5, max_nice)

        # Default random value if type and load don't affect the value
        return random.randint(min_nice, max_nice)

    def generate_args(self) -> str:
        """
        Generate a random command with arguments for a process.

        Returns:
            str: A randomly generated command with arguments.
        """
        commands = {
            "system": ["/usr/bin/systemd", "/sbin/init"],
            "user": ["/bin/bash", "python script.py", "java -jar app.jar"],
            "daemon": ["/usr/sbin/cron", "/usr/sbin/sshd"],
            "interactive": ["vim file.txt", "nano config.cfg"],
            "batch": ["make build", "gcc -o program source.c"],
            "real-time": ["ffmpeg -i input.mp4 output.mp4", "vlc --fullscreen"],
            "zombie": ["<defunct>", "<unknown>"],
            "orphan": ["<orphaned>", "<unknown>"],
            "kernel": ["/usr/bin/kworker", "/usr/bin/ksoftirqd"],
            "foreground": ["top", "htop"],
            "background": ["sleep 100", "nohup long_running_task &"],
        }

        # Generate args based on process type if it affects the value
        if self.type in commands:
            return random.choice(commands[self.type])
        else:
            # If process type does not affect args, generate a generic command
            generic_commands = [
                "/bin/bash",
                "python script.py",
                "java -jar app.jar",
                "/usr/bin/systemd",
                "/usr/sbin/cron",
            ]
            return random.choice(generic_commands)

    def generate_blocked(self) -> str:
        """
        Generate a random hexadecimal mask of blocked signals for a process.

        Returns:
            str: A randomly generated hexadecimal mask of blocked signals.
        """
        # Define ranges for blocked signals based on process type and load
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Higher likelihood of no blocked signals
            return random.choice(["0x00000000", "0x00000001", "0xFFFFFFFF"])
        elif self.type in ["user", "interactive"]:
            # User/interactive processes: Moderate blocked signals
            return f"0x{random.randint(0, 0x0FFFFFFF):08x}"
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Higher blocked signals
            return f"0x{random.randint(0x10000000, 0xFFFFFFFF):08x}"
        elif self.type in ["zombie", "orphan"]:
            # Zombie/orphan processes: No meaningful blocked signals
            return "0x00000000"
        else:
            # Default for other process types
            return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_bsdstart(self) -> str:
        """
        Generate a random start time for a process in BSD-style format.

        Returns:
            str: A randomly generated start time in the format "HH:MM" (if started
                less than 24 hours ago) or "Mmm DD" (if started more than 24 hours ago).
        """

        # Determine the start time range based on process type or load
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Likely to have started a long time ago
            start_time = datetime.now() - timedelta(days=random.randint(1, 365))
        elif self.type in ["user", "interactive"]:
            # User/interactive processes: Likely to have started recently
            start_time = datetime.now() - timedelta(
                hours=random.randint(0, 23), minutes=random.randint(0, 59)
            )
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Could have started anytime
            if random.choice([True, False]):
                start_time = datetime.now() - timedelta(
                    hours=random.randint(0, 23), minutes=random.randint(0, 59)
                )
            else:
                start_time = datetime.now() - timedelta(days=random.randint(1, 365))
        else:
            # Default: Randomly choose between recent or long-ago start times
            if random.choice([True, False]):
                start_time = datetime.now() - timedelta(
                    hours=random.randint(0, 23), minutes=random.randint(0, 59)
                )
            else:
                start_time = datetime.now() - timedelta(days=random.randint(1, 365))

        # Format the start time
        if (datetime.now() - start_time).days < 1:
            # If started less than 24 hours ago, return "HH:MM"
            return start_time.strftime("%H:%M")
        else:
            # If started more than 24 hours ago, return "Mmm DD"
            return start_time.strftime("%b %d")

    def generate_bsdtime(self) -> str:
        """
        Generate a random accumulated CPU time for a process in BSD-style format.

        Returns:
            str: A randomly generated accumulated CPU time in the format "HH:MM:SS".
        """

        # Determine the CPU time range based on process type or load
        if self.load == "light":
            # Light load: Shorter CPU times
            hours = 0
            minutes = random.randint(0, 29)  # Up to 30 minutes
            seconds = random.randint(0, 59)
        elif self.load == "medium":
            # Medium load: Moderate CPU times
            hours = random.randint(0, 5)  # Up to 5 hours
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        elif self.load == "heavy":
            # Heavy load: Longer CPU times
            hours = random.randint(5, 23)  # Between 5 and 23 hours
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        else:
            # If load does not affect the value, generate a generic CPU time
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)

        # Format the time as "HH:MM:SS"
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_c(self) -> int:
        """
        Generate a random processor utilization percentage for a process.

        Returns:
            int: A randomly generated processor utilization percentage between 0 and 100.
        """
        return self.generate_random_value_by_load(
            light=[0, 30], medium=[30, 70], heavy=[70, 100]
        )

    def generate_caught(self) -> str:
        """
        Generate a random hexadecimal mask of caught signals for a process.

        Returns:
            str: A randomly generated hexadecimal mask of caught signals.
        """
        # Define ranges for caught signals based on process type and load
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Likely to have specific caught signals
            return random.choice(["0x00000000", "0x00000001", "0xFFFFFFFF"])
        elif self.type in ["user", "interactive"]:
            # User/interactive processes: Moderate caught signals
            return f"0x{random.randint(0, 0x0FFFFFFF):08x}"
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Higher caught signals
            return f"0x{random.randint(0x10000000, 0xFFFFFFFF):08x}"
        elif self.type in ["zombie", "orphan"]:
            # Zombie/orphan processes: No meaningful caught signals
            return "0x00000000"
        else:
            # Default for other process types or if process type/load is irrelevant
            return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_cgname(self) -> str:
        """
        Generate a random control group name for a process.

        Returns:
            str: A randomly generated control group name based on process type.
        """
        # Define control group names based on process type
        cgname_map = {
            "system": ["system.slice", "init.scope"],
            "user": ["user.slice", "user-1000.slice"],
            "daemon": ["system.slice", "daemon.slice"],
            "interactive": ["user.slice", "interactive.slice"],
            "batch": ["batch.slice", "system.slice"],
            "real-time": ["realtime.slice", "system.slice"],
            "zombie": ["<unknown>", "zombie.slice"],
            "orphan": ["<unknown>", "orphan.slice"],
            "kernel": ["kernel.slice", "system.slice"],
            "foreground": ["user.slice", "foreground.slice"],
            "background": ["background.slice", "system.slice"],
        }

        # Generate cgname based on process type if it affects the value
        if self.type in cgname_map:
            return random.choice(cgname_map[self.type])
        else:
            # Default control group names if process type/load is irrelevant
            default_cgnames = [
                "user.slice",
                "system.slice",
                "init.scope",
                "background.slice",
                "batch.slice",
            ]
            return random.choice(default_cgnames)

    def generate_cgroup(self) -> str:
        """
        Generate a random control group path for a process.

        Returns:
            str: A randomly generated control group path based on process type.
        """

        # Define control group paths based on process type
        cgroup_map = {
            "system": ["/system.slice", "/init.scope"],
            "user": ["/user.slice", "/user-1000.slice"],
            "daemon": ["/system.slice/daemon.slice", "/daemon.slice"],
            "interactive": ["/user.slice/interactive.slice", "/interactive.slice"],
            "batch": ["/batch.slice", "/system.slice/batch.slice"],
            "real-time": ["/realtime.slice", "/system.slice/realtime.slice"],
            "zombie": ["/<unknown>", "/zombie.slice"],
            "orphan": ["/<unknown>", "/orphan.slice"],
            "kernel": ["/kernel.slice", "/system.slice/kernel.slice"],
            "foreground": ["/user.slice/foreground.slice", "/foreground.slice"],
            "background": ["/background.slice", "/system.slice/background.slice"],
        }

        # Generate cgroup based on process type if it affects the value
        if self.type in cgroup_map:
            return random.choice(cgroup_map[self.type])
        else:
            # Default control group paths if process type/load is irrelevant
            default_cgroups = [
                "/user.slice",
                "/system.slice",
                "/init.scope",
                "/background.slice",
                "/batch.slice",
            ]
            return random.choice(default_cgroups)

    def generate_cgroupns(self) -> int:
        """
        Generate a random control group namespace inode number for a process.

        Returns:
            int: A randomly generated control group namespace inode number.
        """
        return self.generate_random_value_based_on_type(
            low=[0, 10000],
            mid=[10001, 40000],
            high=[40001, 65535],
            range=[0, 65535],
            mid_items=["user", "interactive"],
        )

    def generate_class(self) -> str:
        """
        Generate a random scheduling class for a process.

        Returns:
            str: A randomly generated scheduling class based on process type.
        """
        class_map = {
            "system": ["TS", "FF", "IDL"],
            "user": ["TS", "RR", "B"],
            "daemon": ["TS", "B", "IDL"],
            "interactive": ["TS", "RR", "ISO"],
            "batch": ["B", "IDL"],
            "real-time": ["FF", "RR", "DLN"],
            "zombie": ["IDL"],
            "orphan": ["IDL"],
            "kernel": ["TS", "FF", "DLN"],
            "foreground": ["TS", "RR", "ISO"],
            "background": ["B", "IDL"],
        }

        # Generate scheduling class based on process type if it affects the value
        if self.type in class_map:
            return random.choice(class_map[self.type])
        else:
            # Default scheduling classes if process type/load is irrelevant
            default_classes = ["TS", "FF", "RR", "B", "ISO", "IDL", "DLN"]
            return random.choice(default_classes)

    def generate_comm(self) -> str:
        """
        Generate a random command name for a process.

        Returns:
            str: A randomly generated command name based on process type.
        """
        comm_map = {
            "system": ["systemd", "init"],
            "user": ["bash", "python", "java"],
            "daemon": ["cron", "sshd", "nginx"],
            "interactive": ["vim", "nano", "htop"],
            "batch": ["make", "gcc", "build"],
            "real-time": ["ffmpeg", "vlc", "obs"],
            "zombie": ["<defunct>", "<unknown>"],
            "orphan": ["<orphaned>", "<unknown>"],
            "kernel": ["kworker", "ksoftirqd"],
            "foreground": ["top", "htop", "bash"],
            "background": ["sleep", "nohup", "background_task"],
        }

        # Generate comm based on process type if it affects the value
        if self.type in comm_map:
            return random.choice(comm_map[self.type])
        else:
            # Default command names if process type/load is irrelevant
            default_comms = ["bash", "python", "java", "systemd", "cron"]
            return random.choice(default_comms)

    def generate_cp(self) -> float:
        """
        Generate a random CPU utilization percentage for a process.

        Returns:
            float: A randomly generated CPU utilization percentage between 0.0 and 100.0.
        """
        return self.generate_random_value_based_on_load_round(
            light=[0.0, 30.0], medium=[30.0, 70.0], heavy=[70.0, 100.0], round=1
        )

    def generate_cputime(self) -> str:
        """
        Generate a random CPU time for a process in the format [DD-]HH:MM:SS.

        Returns:
            str: A randomly generated CPU time in the format [DD-]HH:MM:SS.
        """
        # Determine the CPU time range based on load
        if self.load == "light":
            # Light load: Shorter CPU times
            days = 0
            hours = 0
            minutes = random.randint(0, 29)  # Up to 30 minutes
            seconds = random.randint(0, 59)
        elif self.load == "medium":
            # Medium load: Moderate CPU times
            days = 0
            hours = random.randint(0, 11)  # Up to 12 hours
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        elif self.load == "heavy":
            # Heavy load: Longer CPU times
            days = random.randint(0, 6)  # Up to 7 days
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        else:
            # If load does not affect the value, generate a generic CPU time
            days = random.randint(0, 6)
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)

        # Format the time as [DD-]HH:MM:SS
        if days > 0:
            return f"{days:02d}-{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_cputimes(self) -> int:
        """
        Generate a random CPU time in seconds for a process.

        Returns:
            int: A randomly generated CPU time in seconds.
        """
        return self.generate_random_value_by_load(
            light=[0, 1800], medium=[1801, 43200], heavy=[43201, 604800]
        )

    def generate_cuc(self) -> float:
        """
        Generate a random CPU utilization percentage for a process.

        Returns:
            float: A randomly generated CPU utilization percentage between 0.0 and 100.0.
        """
        return self.generate_random_value_based_on_load_round(
            light=[0.0, 30.0], medium=[30.0, 70.0], heavy=[70.0, 100.0], round=1
        )

    def generate_cuu(self) -> float:
        """
        Generate a random CPU utilization percentage for a process.

        Returns:
            float: A randomly generated CPU utilization percentage between 0.0 and 100.0.
        """
        return self.generate_random_value_based_on_load_round(
            light=[0.0, 30.0], medium=[30.0, 70.0], heavy=[70.0, 100.0], round=1
        )

    def generate_docker(self) -> str:
        """
        Generate a random Docker container ID for a process.

        Returns:
            str: A randomly generated Docker container ID or "-" if not in a container.
        """
        # Define logic for determining if the process is in a container
        if self.type in ["system", "kernel", "zombie", "orphan"]:
            # These process types are unlikely to be in a container
            return "-"
        elif self.type in ["user", "daemon", "batch", "background"]:
            # These process types are more likely to be in a container
            return "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
        else:
            # Default: Randomly decide if the process is in a container
            if random.choice([True, False]):
                return "".join(
                    random.choices(string.ascii_lowercase + string.digits, k=12)
                )
            else:
                return "-"

    def generate_drs(self) -> int:
        """
        Generate a random disk read size for a process.

        Returns:
            int: A randomly generated disk read size in bytes.
        """
        return self.generate_random_value_by_load(
            light=[1024, 4096], medium=[4097, 16384], heavy=[16385, 65536]
        )

    def generate_egid(self) -> int:
        """
        Generate a random effective group ID for a process.

        Returns:
            int: A randomly generated effective group ID.
        """
        return self.generate_random_value_based_on_type(
            low=[0, 100],
            mid=[1000, 5000],
            high=[500, 1000],
            range=[0, 65535],
        )

    def generate_egroup(self) -> str:
        """
        Generate a random effective group name for a process.

        Returns:
            str: A randomly generated effective group name based on process type.
        """
        # Define group names based on process type
        egroup_map = {
            "system": ["root", "wheel"],
            "user": ["staff", "users", "developers"],
            "daemon": ["daemon", "services"],
            "interactive": ["staff", "users"],
            "batch": ["batch", "build"],
            "real-time": ["realtime", "media"],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["root", "system"],
            "foreground": ["staff", "users"],
            "background": ["background", "services"],
        }

        # Generate egroup based on process type if it affects the value
        if self.type in egroup_map:
            return random.choice(egroup_map[self.type])
        else:
            # Default group names if process type/load is irrelevant
            default_groups = ["staff", "root", "users", "daemon", "services"]
            return random.choice(default_groups)

    def generate_eip(self) -> str:
        """
        Generate a random instruction pointer (EIP) for a process.

        Returns:
            str: A randomly generated instruction pointer in hexadecimal format.
        """
        # Define ranges for eip based on process type
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Likely to have higher memory addresses
            return f"0x{random.randint(0x7FFF0000, 0x7FFFFFFF):08x}"
        elif self.type in ["user", "interactive", "foreground"]:
            # User/interactive processes: Likely to have mid-range memory addresses
            return f"0x{random.randint(0x400000, 0x7FFEFFFF):08x}"
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Likely to have lower memory addresses
            return f"0x{random.randint(0x100000, 0x3FFFFF):08x}"
        elif self.type in ["zombie", "orphan"]:
            # Zombie/orphan processes: Likely to have zeroed or invalid instruction pointers
            return "0x00000000"
        else:
            # Default: Generate a random instruction pointer in the full range
            return f"0x{random.randint(0x100000, 0x7FFFFFFF):08x}"

    def generate_esp(self) -> str:
        """
        Generate a random stack pointer (ESP) for a process.

        Returns:
            str: A randomly generated stack pointer in hexadecimal format.
        """

        # Define ranges for esp based on process type
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Likely to have higher memory addresses
            return f"0x{random.randint(0x7FFF0000, 0x7FFFFFFF):08x}"
        elif self.type in ["user", "interactive", "foreground"]:
            # User/interactive processes: Likely to have mid-range memory addresses
            return f"0x{random.randint(0x400000, 0x7FFEFFFF):08x}"
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Likely to have lower memory addresses
            return f"0x{random.randint(0x100000, 0x3FFFFF):08x}"
        elif self.type in ["zombie", "orphan"]:
            # Zombie/orphan processes: Likely to have zeroed or invalid stack pointers
            return "0x00000000"
        else:
            # Default: Generate a random stack pointer in the full range
            return f"0x{random.randint(0x100000, 0x7FFFFFFF):08x}"

    def generate_etime(self) -> str:
        """
        Generate a random elapsed time for a process in the format [DD-]HH:MM:SS.

        Returns:
            str: A randomly generated elapsed time in the format [DD-]HH:MM:SS.
        """
        if self.load == "light":
            # Light load: Shorter elapsed times
            days = 0
            hours = random.randint(0, 1)  # Up to 1 hour
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        elif self.load == "medium":
            # Medium load: Moderate elapsed times
            days = 0
            hours = random.randint(1, 12)  # Up to 12 hours
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        elif self.load == "heavy":
            # Heavy load: Longer elapsed times
            days = random.randint(0, 7)  # Up to 7 days
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)
        else:
            # If load does not affect the value, generate a generic elapsed time
            days = random.randint(0, 7)
            hours = random.randint(0, 23)
            minutes = random.randint(0, 59)
            seconds = random.randint(0, 59)

        # Format the time as [DD-]HH:MM:SS
        if days > 0:
            return f"{days:02d}-{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_etimes(self) -> int:
        """
        Generate a random elapsed time in seconds for a process.

        Returns:
            int: A randomly generated elapsed time in seconds.
        """
        return self.generate_random_value_by_load(
            light=[0, 3600], medium=[3601, 43200], heavy=[43201, 604800]
        )

    def generate_env(self) -> Dict[str, str]:
        """
        Generate a random dictionary of environment variables for a process.

        Returns:
            Dict[str, str]: A randomly generated dictionary of environment variables.
        """

        # Define base environment variables
        base_env = {
            "PATH": "/usr/bin:/bin",
            "HOME": "/home/user",
            "LANG": "en_US.UTF-8",
        }

        # Add process-specific environment variables
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Likely to have system-level environment variables
            base_env.update(
                {
                    "PATH": "/sbin:/usr/sbin:/usr/bin:/bin",
                    "LANG": "C",
                    "SHELL": "/bin/sh",
                }
            )
        elif self.type in ["user", "interactive", "foreground"]:
            # User/interactive processes: Likely to have user-level environment variables
            base_env.update(
                {
                    "USER": "user",
                    "DISPLAY": ":0",
                    "EDITOR": random.choice(["vim", "nano"]),
                }
            )
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Likely to have service-related environment variables
            base_env.update(
                {
                    "SERVICE_NAME": random.choice(["nginx", "cron", "sshd"]),
                    "LOG_LEVEL": random.choice(["INFO", "DEBUG", "ERROR"]),
                }
            )
        elif self.type in ["zombie", "orphan"]:
            # Zombie/orphan processes: Likely to have minimal or unknown environment variables
            base_env.update(
                {
                    "STATUS": "<unknown>",
                }
            )
        else:
            # Default: Add generic environment variables
            base_env.update(
                {
                    "TEMP": "/tmp",
                    "TERM": random.choice(["xterm", "screen"]),
                }
            )

        return base_env

    def generate_euid(self) -> int:
        """
        Generate a random effective user ID (euid) for a process.

        Returns:
            int: A randomly generated effective user ID (0 to 65535).
        """

        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[1000, 5000], high=[500, 1000], range=[0, 65535]
        )

    def generate_euser(self) -> str:
        """
        Generate a random effective user name (euser) for a process.

        Returns:
            str: A randomly generated effective user name.
        """
        user_map = {
            "system": ["root", "system"],
            "user": ["user1", "user2", "developer"],
            "daemon": ["daemon", "service"],
            "interactive": ["user1", "user2"],
            "batch": ["builder", "compiler"],
            "real-time": ["media", "streamer"],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["root", "system"],
            "foreground": ["user1", "user2"],
            "background": ["background", "service"],
        }

        if self.type in user_map:
            return random.choice(user_map[self.type])
        else:
            default_users = ["user1", "user2", "root", "daemon"]
            return random.choice(default_users)

    def generate_exe(self) -> str:
        """
        Generate a random executable path for a process.

        Returns:
            str: A randomly generated executable path based on process type.
        """

        exe_map = {
            "system": ["/usr/bin/systemd", "/sbin/init"],
            "user": ["/bin/bash", "/usr/bin/python", "/usr/bin/java"],
            "daemon": ["/usr/sbin/cron", "/usr/sbin/sshd"],
            "interactive": ["/usr/bin/vim", "/usr/bin/nano"],
            "batch": ["/usr/bin/make", "/usr/bin/gcc"],
            "real-time": ["/usr/bin/ffmpeg", "/usr/bin/vlc"],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["/usr/bin/kworker", "/usr/bin/ksoftirqd"],
            "foreground": ["/usr/bin/top", "/usr/bin/htop"],
            "background": ["/bin/sleep", "/usr/bin/nohup"],
        }

        if self.type in exe_map:
            return random.choice(exe_map[self.type])
        else:
            default_exes = ["/bin/bash", "/usr/bin/python", "/usr/bin/java"]
            return random.choice(default_exes)

    def generate_fds(self) -> int:
        """
        Generate a random number of open file descriptors (fds) for a process.

        Returns:
            int: A randomly generated number of open file descriptors.
        """
        # Define ranges for fds based on process type and load
        if self.type in ["system", "kernel"]:
            # System/kernel processes: Likely to have a higher number of open file descriptors
            return random.randint(100, 1000)
        elif self.type in ["user", "interactive", "foreground"]:
            # User/interactive processes: Likely to have a moderate number of open file descriptors
            return random.randint(10, 100)
        elif self.type in ["daemon", "batch", "background"]:
            # Daemon/batch/background processes: Likely to have a higher number of open file descriptors
            return random.randint(50, 500)
        elif self.type in ["zombie", "orphan"]:
            # Zombie/orphan processes: Likely to have no open file descriptors
            return 0
        else:
            # Default: Generate a random number of open file descriptors in a generic range
            return random.randint(0, 1000)

    def generate_fgid(self) -> int:
        """
        Generate a random file group ID (fgid) for a process.

        Returns:
            int: A randomly generated file group ID (0 to 65535).
        """
        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[1000, 5000], high=[500, 1000], range=[0, 65535]
        )

    def generate_fgroup(self) -> str:
        """
        Generate a random file group name (fgroup) for a process.

        Returns:
            str: A randomly generated file group name based on process type.
        """
        fgroup_map = {
            "system": ["root", "wheel"],
            "user": ["staff", "users", "developers"],
            "daemon": ["daemon", "services"],
            "interactive": ["staff", "users"],
            "batch": ["batch", "build"],
            "real-time": ["realtime", "media"],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["root", "system"],
            "foreground": ["staff", "users"],
            "background": ["background", "services"],
        }

        if self.type in fgroup_map:
            return random.choice(fgroup_map[self.type])
        else:
            return random.choice(["staff", "root", "users", "daemon", "services"])

    def generate_fname(self) -> str:
        """
        Generate a random file name (fname) for a process.

        Returns:
            str: A randomly generated file name based on process type.
        """
        fname_map = {
            "system": ["systemd", "init"],
            "user": ["bash", "python", "java"],
            "daemon": ["cron", "sshd", "nginx"],
            "interactive": ["vim", "nano", "htop"],
            "batch": ["make", "gcc", "build"],
            "real-time": ["ffmpeg", "vlc", "obs"],
            "zombie": ["<defunct>", "<unknown>"],
            "orphan": ["<orphaned>", "<unknown>"],
            "kernel": ["kworker", "ksoftirqd"],
            "foreground": ["top", "htop", "bash"],
            "background": ["sleep", "nohup", "background"],
        }

        # Generate fname based on process type if it affects the value
        if self.type in fname_map:
            return random.choice(fname_map[self.type])[:8]
        else:
            # Default executable names if process type/load is irrelevant
            default_fnames = ["bash", "python", "java", "systemd", "cron"]
            return random.choice(default_fnames)[:8]

    def generate_fuid(self) -> int:
        """
        Generate a random file user ID (fuid) for a process.

        Returns:
            int: A randomly generated file user ID (0 to 65535).
        """
        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[1000, 5000], high=[500, 1000], range=[0, 65535]
        )

    def generate_fuser(self) -> str:
        """
        Generate a random file user name (fuser) for a process.

        Returns:
            str: A randomly generated file user name based on process type.
        """
        # Define user names based on process type
        fuser_map = {
            "system": ["root", "system"],
            "user": ["user", "developer", "guest"],
            "daemon": ["daemon", "service"],
            "interactive": ["user", "admin"],
            "batch": ["builder", "compiler"],
            "real-time": ["media", "streamer"],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["root", "system"],
            "foreground": ["user", "admin"],
            "background": ["background", "service"],
        }

        # Generate fuser based on process type if it affects the value
        if self.type in fuser_map:
            return random.choice(fuser_map[self.type])
        else:
            # Default user names if process type/load is irrelevant
            default_users = ["root", "user", "nobody", "daemon"]
            return random.choice(default_users)

    def generate_gid(self) -> int:
        """
        Generate a random group ID (gid) for a process.

        Returns:
            int: A randomly generated group ID (0 to 65535).
        """
        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[1000, 5000], high=[500, 1000], range=[0, 65535]
        )

    def generate_group(self) -> str:
        """
        Generate a random group name for a process.

        Returns:
            str: A randomly generated group name based on process type.
        """
        group_map = {
            "system": ["root", "wheel"],
            "user": ["staff", "users", "developers"],
            "daemon": ["daemon", "services"],
            "interactive": ["staff", "users"],
            "batch": ["batch", "build"],
            "real-time": ["realtime", "media"],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["root", "system"],
            "foreground": ["staff", "users"],
            "background": ["background", "services"],
        }

        if self.type in group_map:
            return random.choice(group_map[self.type])
        else:
            return random.choice(["staff", "root", "users", "daemon", "services"])

    def generate_htprv(self) -> int:
        """
        Generate a random high-priority value for a process.

        Returns:
            int: A randomly generated high-priority value between 0 and 100.
        """
        return random.randint(0, 100)

    def generate_htshr(self) -> int:
        """
        Generate a random high-threshold share value for a process.

        Returns:
            int: A randomly generated high-threshold share value between 0 and 100.
        """
        return random.randint(0, 100)

    def generate_ignored(self) -> str:
        """
        Gererate a random ignored value for a process.

        Returns:
            str: A randomly generated ignored value, typically a hexadecimal string.
        """
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_ipcns(self) -> int:
        """
        Generate a random IPC namespace inode number for a process.

        Returns:
            int: A randomly generated IPC namespace inode number.
        """
        return random.randint(0, 65535)

    def generate_label(self) -> str:
        """
        Generate a random SELinux label for a process.

        Returns:
            str: A randomly generated SELinux label based on process type.
        """
        label_map = {
            "system": ["system_u:system_r:init_t:s0", "system_u:system_r:sshd_t:s0"],
            "user": [
                "unconfined_u:unconfined_r:unconfined_t:s0",
                "user_u:user_r:user_t:s0",
            ],
            "daemon": ["system_u:system_r:cron_t:s0", "system_u:system_r:nginx_t:s0"],
            "interactive": [
                "user_u:user_r:user_t:s0",
                "unconfined_u:unconfined_r:unconfined_t:s0",
            ],
            "batch": [
                "system_u:system_r:build_t:s0",
                "system_u:system_r:compiler_t:s0",
            ],
            "real-time": [
                "system_u:system_r:media_t:s0",
                "system_u:system_r:streamer_t:s0",
            ],
            "zombie": ["<unknown>"],
            "orphan": ["<unknown>"],
            "kernel": ["system_u:system_r:kernel_t:s0"],
            "foreground": ["user_u:user_r:user_t:s0"],
            "background": ["system_u:system_r:background_t:s0"],
        }

        if self.type in label_map:
            return random.choice(label_map[self.type])
        else:
            return random.choice(
                [
                    "system_u:system_r:init_t:s0",
                    "unconfined_u:unconfined_r:unconfined_t:s0",
                ]
            )

    def generate_lstart(self) -> str:
        """
        Generate a random start time for a process.

        Returns:
            str: A randomly generated start time in the format "Day Mon DD HH:MM:SS YYYY".
        """
        start_time = datetime.now() - timedelta(
            seconds=random.randint(0, 604800)
        )  # Up to 7 days ago
        return start_time.strftime("%a %b %d %H:%M:%S %Y")

    def generate_lsession(self) -> int:
        """
        Generate a random session ID for a process.

        Returns:
            int: A randomly generated session ID (0 to 65535).
        """
        return random.randint(0, 65535)

    def generate_luid(self) -> int:
        """
        Generate a random login user ID (luid) for a process.

        Returns:
            int: A randomly generated login user ID (0 to 65535).
        """

        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[1000, 5000], high=[500, 1000], range=[0, 65535]
        )

    def generate_lwp(self) -> int:
        """
        Generate a random lightweight process ID (lwp) for a process.

        Returns:
            int: A randomly generated lightweight process ID (1 to 65535).
        """
        return random.randint(1, 65535)

    def generate_lxc(self) -> str:
        """
        Generate a random LXC container ID for a process.

        Returns:
            str: A randomly generated LXC container ID or "-" if not in a container.
        """
        if self.type in ["system", "kernel", "zombie", "orphan"]:
            return "-"  # Not in a container
        else:
            return "".join(
                random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12)
            )  # Random container ID

    def generate_machine(self) -> str:
        """
        Generate a random machine architecture for a process.

        Returns:
            str: A randomly generated machine architecture.
        """
        return random.choice(["x86_64", "arm64", "i386", "ppc64", "riscv"])

    def generate_maj_flt(self) -> int:
        """
        Generate a random number of major page faults for a process.

        Returns:
            int: A randomly generated number of major page faults."""
        return random.randint(0, 1000)

    def generate_min_flt(self) -> int:
        """
        Generate a random number of minor page faults for a process.

        Returns:
            int: A randomly generated number of minor page faults.
        """
        return random.randint(0, 1000000)

    def generate_mntns(self) -> int:
        """
        Generate a random mount namespace inode number for a process.

        Returns:
            int: A randomly generated mount namespace inode number.
        """
        return self.generate_random_value_based_on_type(
            low=[0, 1000], mid=[1001, 5000], high=[5001, 10000], range=[0, 65535]
        )

    def generate_netns(self) -> int:
        """
        Generate a random network namespace inode number for a process.

        Returns:
            int: A randomly generated network namespace inode number.
        """
        return random.randint(0, 65535)

    def generate_ni(self) -> int:
        """
        Generate a random nice value (ni) for a process.

        Returns:
            int: A randomly generated nice value (-20 to 19).
        """

        return self.generate_random_value_based_on_type(
            low=[-20, -20], mid=[0, 10], high=[10, 19], range=[-20, 19]
        )

    def generate_nlwp(self) -> int:
        """
        Generate a random number of lightweight processes (nlwp) for a process.

        Returns:
            int: A randomly generated number of lightweight processes.
        """

        if self.type in ["system", "kernel"]:
            return random.randint(
                10, 100
            )  # System/kernel processes often have more threads
        elif self.type in ["user", "interactive", "foreground"]:
            return random.randint(1, 10)  # User processes typically have fewer threads
        elif self.type in ["daemon", "batch", "background"]:
            return random.randint(5, 50)  # Daemon processes may have moderate threads
        else:
            return random.randint(1, 100)  # Default range

    def generate_numa(self) -> int:
        """
        Generate a random NUMA node (numa) for a process.

        Returns:
            int: A randomly generated NUMA node.
        """
        return random.randint(0, 3)  # Assuming a system with up to 4 NUMA nodes

    def generate_nwchan(self) -> str:
        """
        Generate a random wait channel (nwchan) for a process.

        Returns:
            str: A randomly generated wait channel or "-".
        """

        if self.type in ["zombie", "orphan"]:
            return "-"  # No wait channel
        else:
            return random.choice(
                ["do_wait", "poll_schedule_timeout", "io_schedule", "-"]
            )

    def generate_oom(self) -> int:
        """
        Generate a random Out of Memory (OOM) score for a process.

        Returns:
            int: A randomly generated OOM score (0 to 1000).
        """
        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[100, 500], high=[500, 1000], range=[0, 1000]
        )

    def generate_oomadj(self) -> int:
        """
        Generate a random OOM adjustment value (oomadj) for a process.

        Returns:
            int: A randomly generated OOM adjustment value (-1000 to 1000).
        """
        return self.generate_random_value_based_on_type(
            low=[-1000, -1000], mid=[-500, 0], high=[0, 500], range=[-1000, 1000]
        )

    def generate_ouid(self) -> int:
        """
        Generate a random owner user ID (ouid) for a process.

        Returns:
            int: A randomly generated owner user ID (0 to 65535).
        """
        return self.generate_random_value_based_on_type(
            low=[0, 0], mid=[1000, 5000], high=[500, 1000], range=[0, 65535]
        )

    def generate_pcap(self) -> str:
        """
        Generate a random process capabilities bitmask (pcap) for a process.

        Returns:
            str: A randomly generated process capabilities bitmask.
        """

        if self.type in ["system", "kernel"]:
            return "0xFFFFFFFF"  # Full capabilities
        elif self.type in ["user", "interactive", "foreground"]:
            return "0x00000001"  # Limited capabilities
        elif self.type in ["daemon", "batch", "background"]:
            return "0x00000010"  # Service-related capabilities
        else:
            return f"0x{random.randint(0, 0xFFFFFFFF):08x}"  # Default range

    def generate_pcaps(self) -> str:
        """
        Generate a random process capabilities bitmask (pcaps) for a process.

        Returns:
            str: A randomly generated process capabilities bitmask.
        """

        if self.type in ["system", "kernel"]:
            return "0xFFFFFFFF"  # Full capabilities
        elif self.type in ["user", "interactive", "foreground"]:
            return "0x00000001"  # Limited capabilities
        elif self.type in ["daemon", "batch", "background"]:
            return "0x00000010"  # Service-related capabilities
        else:
            return f"0x{random.randint(0, 0xFFFFFFFF):08x}"  # Default range

    def generate_pcpu(self) -> float:
        """
        Generate a random CPU utilization percentage (pcpu) for a process.

        Returns:
            float: A randomly generated CPU utilization percentage (0.0 to 100.0).
        """

        return self.generate_random_value_based_on_load_round(
            light=[0.0, 30.0], medium=[30.1, 70.0], heavy=[70.1, 100.0], round=1
        )

    def generate_pending(self) -> str:
        """
        Generate a random mask of pending signals (pending) for a process.

        Returns:
            str: A randomly generated mask of pending signals.
        """
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_pgid(self) -> int:
        """
        Generate a random process group ID (pgid) for a process.

        Returns:
            int: A randomly generated process group ID (0 to 65535).
        """
        return random.randint(0, 65535)

    def generate_pgrp(self) -> int:
        """
        Generate a random process group ID (pgrp) for a process.

        Returns:
            int: A randomly generated process group ID (0 to 65535).
        """
        return self.pgid  # Alias for `pgid`

    def generate_pidns(self) -> int:
        """
        Generate a random PID namespace inode number (pidns) for a process.

        Returns:
            int: A randomly generated PID namespace inode number.
        """
        return random.randint(0, 65535)

    def generate_pmem(self) -> float:
        """
        Generate a random memory utilization percentage (pmem) for a process.

        Returns:
            float: A randomly generated memory utilization percentage (0.0 to 100.0).
        """
        return self.generate_random_value_based_on_load_round(
            light=[0.0, 30.0], medium=[30.1, 70.0], heavy=[70.1, 100.0], round=1
        )

    def generate_policy(self) -> str:
        """
        Generate a random scheduling policy (policy) for a process.

        Returns:
            str: A randomly generated scheduling policy.
        """
        process_type = getattr(self, "process_type", None)

        policy_map = {
            "system": ["SCHED_OTHER", "SCHED_FIFO"],
            "user": ["SCHED_OTHER", "SCHED_BATCH"],
            "daemon": ["SCHED_BATCH", "SCHED_IDLE"],
            "interactive": ["SCHED_OTHER", "SCHED_RR"],
            "batch": ["SCHED_BATCH"],
            "real-time": ["SCHED_FIFO", "SCHED_RR", "SCHED_DEADLINE"],
            "zombie": ["SCHED_IDLE"],
            "orphan": ["SCHED_IDLE"],
            "kernel": ["SCHED_OTHER", "SCHED_FIFO"],
            "foreground": ["SCHED_OTHER", "SCHED_RR"],
            "background": ["SCHED_BATCH", "SCHED_IDLE"],
        }

        if process_type in policy_map:
            return random.choice(policy_map[process_type])
        else:
            return random.choice(
                [
                    "SCHED_OTHER",
                    "SCHED_FIFO",
                    "SCHED_RR",
                    "SCHED_BATCH",
                    "SCHED_IDLE",
                    "SCHED_DEADLINE",
                ]
            )

    def generate_ppid(self) -> int:
        """
        Generate a random parent process ID (ppid) for a process.

        Returns:
            int: A randomly generated parent process ID (1 to 65535).
        """
        return random.randint(1, 65535)

    def generate_pri(self) -> int:
        """
        Generate a random priority value for a process.

        Returns:
            int: A randomly generated priority value (0 to 139).
        """
        return random.randint(0, 139)

    def generate_psr(self) -> int:
        return random.randint(0, 7)  # Adjust the range based on the number of CPUs

    def generate_pss(self) -> int:
        """
        Generate a random proportional set size (pss) for a process.

        Returns:
            int: A randomly generated proportional set size in kilobytes.
        """
        return random.randint(1024, 65536)  # Memory in KB

    def generate_rbytes(self) -> int:
        """
        Generate a random number of bytes read (rbytes) for a process.

        Returns:
            int: A randomly generated number of bytes read.
        """
        return random.randint(0, 1048576)  # Bytes read (up to 1 MB)

    def generate_rchars(self) -> int:
        """
        Generate a random number of characters read (rchars) for a process.

        Returns:
            int: A randomly generated number of characters read.
        """
        return random.randint(0, 1048576)  # Characters read (up to 1 MB)

    def generate_rgid(self) -> int:
        """
        Generate a random real group ID (rgid) for a process.

        Returns:
            int: A randomly generated real group ID (0 to 65535).
        """
        return random.randint(0, 65535)

    def generate_rgroup(self) -> str:
        """
        Generate a random real group name (rgroup) for a process.

        Returns:
            str: A randomly generated real group name.
        """
        return random.choice(["staff", "root", "users", "daemon", "services"])

    def generate_rops(self) -> int:
        """
        Generate a random number of read operations (rops) for a process.

        Returns:
            int: A randomly generated number of read operations.
        """
        return random.randint(0, 10000)

    def generate_rss(self) -> int:
        """
        Generate a random resident set size (rss) for a process.

        Returns:
            int: A randomly generated resident set size in kilobytes.
        """
        return random.randint(1024, 65536)  # Memory in KB

    def generate_rssize(self) -> int:
        """
        Generate a random resident set size (rssize) for a process.

        Returns:
            int: A randomly generated resident set size in kilobytes.
        """
        return self.rss()  # Alias for `rss`

    def generate_rsz(self) -> int:
        """
        Generate a random resident size (rsz) for a process.

        Returns:
            int: A randomly generated resident size in kilobytes.
        """
        return self.rss  # Alias for `rss`

    def generate_rtprio(self) -> int:
        """
        Generate a random real-time priority (rtprio) for a process.

        Returns:
            int: A randomly generated real-time priority (0 to 99).
        """
        return random.randint(0, 99)

    def generate_ruid(self) -> int:
        """
        Generate a random real user ID (ruid) for a process.

        Returns:
            int: A randomly generated real user ID (0 to 65535).
        """
        return random.randint(0, 65535)

    def generate_ruser(self) -> str:
        """
        Generate a random real user name (ruser) for a process.

        Returns:
            str: A randomly generated real user name.
        """
        return random.choice(["root", "user", "nobody", "daemon"])

    def generate_s(self) -> str:
        """
        Generate a random process state (s) for a process.

        Returns:
            str: A randomly generated process state.
        """
        return random.choice(["R", "S", "D", "Z", "T", "X"])

    def generate_sched(self) -> str:
        """
        Generate a random scheduling policy (sched) for a process.

        Returns:
            str: A randomly generated scheduling policy.
        """
        return random.choice(
            [
                "SCHED_OTHER",
                "SCHED_FIFO",
                "SCHED_RR",
                "SCHED_BATCH",
                "SCHED_IDLE",
                "SCHED_DEADLINE",
            ]
        )

    def generate_seat(self) -> str:
        """
        Generate a random seat name (seat) for a process.

        Returns:
            str: A randomly generated seat name.
        """
        return random.choice(["seat0", "seat1", "seat2"])

    def generate_sess(self) -> int:
        """Generate a random session ID (sess) for a process."""
        return random.randint(0, 65535)

    def generate_sgi_p(self) -> int:
        """Generate a random scheduling priority (sgi_p) for a process."""
        return random.randint(0, 139)

    def generate_sgid(self) -> int:
        """Generate a random saved group ID (sgid) for a process."""
        return random.randint(0, 65535)

    def generate_sid(self) -> int:
        """Generate a random session ID (sid) for a process."""
        return random.randint(0, 65535)

    def generate_sig(self) -> str:
        """Generate a random mask of pending signals (sig) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigcatch(self) -> str:
        """Generate a random mask of caught signals (sigcatch) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigignore(self) -> str:
        """Generate a random mask of ignored signals (sigignore) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigmask(self) -> str:
        """Generate a random mask of blocked signals (sigmask) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_size(self) -> int:
        """Generate a random virtual memory size (size) for a process."""
        return random.randint(1024, 1048576)  # Memory in KB

    def generate_slice(self) -> str:
        """Generate a random slice name (slice) for a process."""
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_spid(self) -> int:
        """Generate a random parent process ID (spid) for a process."""
        return random.randint(1, 65535)

    def generate_stackp(self) -> str:
        """Generate a random stack pointer (stackp) for a process."""
        return f"0x{random.randint(0x100000, 0x7FFFFFFF):08x}"

    def generate_start(self) -> str:
        """Generate a random start time (start) for a process."""
        start_time = datetime.now() - timedelta(
            seconds=random.randint(0, 604800)
        )  # Up to 7 days ago
        return start_time.strftime("%Y-%m-%d %H:%M:%S")

    def generate_start_time(self) -> int:
        """Generate a random start time in seconds since epoch (start_time) for a process."""
        return int(
            (datetime.now() - timedelta(seconds=random.randint(0, 604800))).timestamp()
        )

    def generate_stat(self) -> str:
        """Generate a random process state (stat) for a process."""
        return random.choice(["R", "S", "D", "Z", "T", "X"])

    def generate_state(self) -> str:
        """Generate a random process state (state) for a process."""
        return self.generate_stat()  # Alias for `stat`

    def generate_stime(self) -> int:
        """Generate a random system time (stime) for a process."""
        return random.randint(0, 100000)  # Time in jiffies

    def generate_suid(self) -> int:
        """Generate a random saved user ID (suid) for a process."""
        return random.randint(0, 65535)

    def generate_supgid(self) -> list:
        """Generate a random list of supplementary group IDs (supgid) for a process."""
        return [random.randint(0, 65535) for _ in range(random.randint(1, 5))]

    def generate_sess(self) -> int:
        """Generate a random session ID (sess) for a process."""
        return random.randint(0, 65535)

    def generate_sgi_p(self) -> int:
        """Generate a random scheduling priority (sgi_p) for a process."""
        return random.randint(0, 139)

    def generate_sgid(self) -> int:
        """Generate a random saved group ID (sgid) for a process."""
        return random.randint(0, 65535)

    def generate_sid(self) -> int:
        """Generate a random session ID (sid) for a process."""
        return random.randint(0, 65535)

    def generate_sig(self) -> str:
        """Generate a random mask of pending signals (sig) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigcatch(self) -> str:
        """Generate a random mask of caught signals (sigcatch) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigignore(self) -> str:
        """Generate a random mask of ignored signals (sigignore) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigmask(self) -> str:
        """Generate a random mask of blocked signals (sigmask) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_size(self) -> int:
        """Generate a random virtual memory size (size) for a process."""
        return random.randint(1024, 1048576)  # Memory in KB

    def generate_slice(self) -> str:
        """Generate a random slice name (slice) for a process."""
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_spid(self) -> int:
        """Generate a random parent process ID (spid) for a process."""
        return random.randint(1, 65535)

    def generate_stackp(self) -> str:
        """Generate a random stack pointer (stackp) for a process."""
        return f"0x{random.randint(0x100000, 0x7FFFFFFF):08x}"

    def generate_start(self) -> str:
        """Generate a random start time (start) for a process."""
        start_time = datetime.now() - timedelta(
            seconds=random.randint(0, 604800)
        )  # Up to 7 days ago
        return start_time.strftime("%Y-%m-%d %H:%M:%S")

    def generate_start_time(self) -> int:
        """Generate a random start time in seconds since epoch (start_time) for a process."""
        return int(
            (datetime.now() - timedelta(seconds=random.randint(0, 604800))).timestamp()
        )

    def generate_stat(self) -> str:
        """Generate a random process state (stat) for a process."""
        return random.choice(["R", "S", "D", "Z", "T", "X"])

    def generate_state(self) -> str:
        """Generate a random process state (state) for a process."""
        return self.generate_stat()  # Alias for `stat`

    def generate_stime(self) -> int:
        """Generate a random system time (stime) for a process."""
        return random.randint(0, 100000)  # Time in jiffies

    def generate_suid(self) -> int:
        """Generate a random saved user ID (suid) for a process."""
        return random.randint(0, 65535)

    def generate_supgid(self) -> list:
        """Generate a random list of supplementary group IDs (supgid) for a process."""
        return [random.randint(0, 65535) for _ in range(random.randint(1, 5))]

    def generate_sess(self) -> int:
        """Generate a random session ID (sess) for a process."""
        return random.randint(0, 65535)

    def generate_sgi_p(self) -> int:
        """Generate a random scheduling priority (sgi_p) for a process."""
        return random.randint(0, 139)

    def generate_sgid(self) -> int:
        """Generate a random saved group ID (sgid) for a process."""
        return random.randint(0, 65535)

    def generate_sid(self) -> int:
        """Generate a random session ID (sid) for a process."""
        return random.randint(0, 65535)

    def generate_sig(self) -> str:
        """Generate a random mask of pending signals (sig) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigcatch(self) -> str:
        """Generate a random mask of caught signals (sigcatch) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigignore(self) -> str:
        """Generate a random mask of ignored signals (sigignore) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_sigmask(self) -> str:
        """Generate a random mask of blocked signals (sigmask) for a process."""
        return f"0x{random.randint(0, 0xFFFFFFFF):08x}"

    def generate_size(self) -> int:
        """Generate a random virtual memory size (size) for a process."""
        return random.randint(1024, 1048576)  # Memory in KB

    def generate_slice(self) -> str:
        """Generate a random slice name (slice) for a process."""
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_spid(self) -> int:
        """Generate a random parent process ID (spid) for a process."""
        return random.randint(1, 65535)

    def generate_stackp(self) -> str:
        """Generate a random stack pointer (stackp) for a process."""
        return f"0x{random.randint(0x100000, 0x7FFFFFFF):08x}"

    def generate_start(self) -> str:
        """Generate a random start time (start) for a process."""
        start_time = datetime.now() - timedelta(
            seconds=random.randint(0, 604800)
        )  # Up to 7 days ago
        return start_time.strftime("%Y-%m-%d %H:%M:%S")

    def generate_start_time(self) -> int:
        """Generate a random start time in seconds since epoch (start_time) for a process."""
        return int(
            (datetime.now() - timedelta(seconds=random.randint(0, 604800))).timestamp()
        )

    def generate_stat(self) -> str:
        """Generate a random process state (stat) for a process."""
        return random.choice(["R", "S", "D", "Z", "T", "X"])

    def generate_state(self) -> str:
        """Generate a random process state (state) for a process."""
        return self.generate_stat()  # Alias for `stat`

    def generate_stime(self) -> int:
        """Generate a random system time (stime) for a process."""
        return random.randint(0, 100000)  # Time in jiffies

    def generate_suid(self) -> int:
        """Generate a random saved user ID (suid) for a process."""
        return random.randint(0, 65535)

    def generate_supgid(self) -> list:
        """Generate a random list of supplementary group IDs (supgid) for a process."""
        return [random.randint(0, 65535) for _ in range(random.randint(1, 5))]

    def generate_supgrp(self) -> list:
        """
        Generate a random list of supplementary group names (supgrp) for a process.
        Return Type: list[str]
        """
        return random.sample(
            ["staff", "root", "users", "daemon", "services"], random.randint(1, 3)
        )

    def generate_suser(self) -> str:
        """
        Generate a random saved user name (suser) for a process.
        Return Type: str
        """
        return random.choice(["root", "user", "nobody", "daemon"])

    def generate_svgid(self) -> int:
        """
        Generate a random saved group ID (svgid) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_svuid(self) -> int:
        """
        Generate a random saved user ID (svuid) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_trs(self) -> int:
        """
        Generate a random text resident set size (trs) for a process.
        Return Type: int
        """
        return random.randint(1024, 65536)  # Memory in KB

    def generate_tt(self) -> str:
        """
        Generate a random controlling terminal (tt) for a process.
        Return Type: str
        """
        return random.choice(["tty1", "tty2", "pts/0", "pts/1", "-"])

    def generate_ucmd(self) -> str:
        """
        Generate a random command name (ucmd) for a process.
        Return Type: str
        """
        return random.choice(["bash", "python", "java", "nginx", "sshd"])

    def generate_ucomm(self) -> str:
        """
        Generate a random command name (ucomm) for a process.
        Return Type: str
        """
        return self.generate_ucmd()  # Alias for `ucmd`

    def generate_uid(self) -> int:
        """
        Generate a random user ID (uid) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_uname(self) -> str:
        """
        Generate a random user name (uname) for a process.
        Return Type: str
        """
        return random.choice(["root", "user", "nobody", "daemon"])

    def generate_unit(self) -> str:
        """
        Generate a random systemd unit name (unit) for a process.
        Return Type: str
        """
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_user(self) -> str:
        """
        Generate a random user name (user) for a process.
        Return Type: str
        """
        return self.generate_uname()  # Alias for `uname`

    def generate_userns(self) -> int:
        """
        Generate a random user namespace inode number (userns) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_uss(self) -> int:
        """
        Generate a random unique set size (uss) for a process.
        Return Type: int
        """
        return random.randint(1024, 65536)  # Memory in KB

    def generate_utsns(self) -> int:
        """
        Generate a random UTS namespace inode number (utsns) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_uunit(self) -> str:
        """
        Generate a random user unit name (uunit) for a process.
        Return Type: str
        """
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_vsize(self) -> int:
        """
        Generate a random virtual memory size (vsize) for a process.
        Return Type: int
        """
        return random.randint(1024, 1048576)  # Memory in KB

    def generate_sz(self) -> int:
        """
        Generate a random virtual memory size (sz) for a process.
        Return Type: int
        """
        return random.randint(1024, 1048576)  # Memory in KB

    def generate_tgid(self) -> int:
        """
        Generate a random thread group ID (tgid) for a process.
        Return Type: int
        """
        return random.randint(1, 65535)

    def generate_thcount(self) -> int:
        """
        Generate a random thread count (thcount) for a process.
        Return Type: int
        """
        return random.randint(1, 100)  # Number of threads

    def generate_tid(self) -> int:
        """
        Generate a random thread ID (tid) for a process.
        Return Type: int
        """
        return random.randint(1, 65535)

    def generate_timens(self) -> int:
        """
        Generate a random time namespace inode number (timens) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_times(self) -> str:
        """
        Generate a random cumulative CPU time (times) for a process.
        Return Type: str
        """
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_tname(self) -> str:
        """
        Generate a random thread name (tname) for a process.
        Return Type: str
        """
        return random.choice(["main", "worker", "io_thread", "render_thread"])

    def generate_tpgid(self) -> int:
        """
        Generate a random terminal process group ID (tpgid) for a process.
        Return Type: int
        """
        return random.randint(1, 65535)

    def generate_trs(self) -> int:
        """
        Generate a random text resident set size (trs) for a process.
        Return Type: int
        """
        return random.randint(1024, 65536)  # Memory in KB

    def generate_tt(self) -> str:
        """
        Generate a random controlling terminal (tt) for a process.
        Return Type: str
        """
        return random.choice(["tty1", "tty2", "pts/0", "pts/1", "-"])

    def generate_ucmd(self) -> str:
        """
        Generate a random command name (ucmd) for a process.
        Return Type: str
        """
        return random.choice(["bash", "python", "java", "nginx", "sshd"])

    def generate_ucomm(self) -> str:
        """
        Generate a random command name (ucomm) for a process.
        Return Type: str
        """
        return self.generate_ucmd()  # Alias for `ucmd`

    def generate_uid(self) -> int:
        """
        Generate a random user ID (uid) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_uname(self) -> str:
        """
        Generate a random user name (uname) for a process.
        Return Type: str
        """
        return random.choice(["root", "user", "nobody", "daemon"])

    def generate_unit(self) -> str:
        """
        Generate a random systemd unit name (unit) for a process.
        Return Type: str
        """
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_user(self) -> str:
        """
        Generate a random user name (user) for a process.
        Return Type: str
        """
        return self.generate_uname()  # Alias for `uname`

    def generate_userns(self) -> int:
        """
        Generate a random user namespace inode number (userns) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_uss(self) -> int:
        """
        Generate a random unique set size (uss) for a process.
        Return Type: int
        """
        return random.randint(1024, 65536)  # Memory in KB

    def generate_utsns(self) -> int:
        """
        Generate a random UTS namespace inode number (utsns) for a process.
        Return Type: int
        """
        return random.randint(0, 65535)

    def generate_uunit(self) -> str:
        """
        Generate a random user unit name (uunit) for a process.
        Return Type: str
        """
        return random.choice(["user.slice", "system.slice", "background.slice"])

    def generate_vsize(self) -> int:
        """
        Generate a random virtual memory size (vsize) for a process.
        Return Type: int
        """
        return random.randint(1024, 1048576)  # Memory in KB

    def generate_wbytes(self) -> int:
        """
        Generate a random number of bytes written (wbytes) for a process.
        Return Type: int
        """
        return random.randint(0, 1048576)  # Bytes written (up to 1 MB)

    def generate_wcbytes(self) -> int:
        """
        Generate a random number of cancelled write bytes (wcbytes) for a process.
        Return Type: int
        """
        return random.randint(0, 1048576)  # Cancelled write bytes (up to 1 MB)

    def generate_wchars(self) -> int:
        """
        Generate a random number of characters written (wchars) for a process.
        Return Type: int
        """
        return random.randint(0, 1048576)  # Characters written (up to 1 MB)

    def generate_wops(self) -> int:
        """
        Generate a random number of write operations (wops) for a process.
        Return Type: int
        """
        return random.randint(0, 10000)  # Number of write operations

    def generate_f(self) -> str:
        """
        Generate a random process flag (f) for a process.
        Return Type: str
        """
        return random.choice(["0x00000000", "0x00000001", "0xFFFFFFFF"])

    def generate_time(self) -> str:
        """
        Generate a random cumulative CPU time (time) for a process.
        Return Type: str
        """
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_wchan(self) -> str:
        if self.type in ["zombie", "orphan"]:
            return "-"  # No kernel function
        else:
            return random.choice(
                ["do_wait", "poll_schedule_timeout", "io_schedule", "-"]
            )
