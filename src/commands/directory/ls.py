from models.file_system import FileSystem
from commands.base import CommandBase
from utils.parser import (
    ParsedCommand,
)
from models.file import File
from models.directory import Directory
from typing import TypedDict, Literal

import datetime


# Types
class MaxWidths(TypedDict):
    perm: int
    owner: int
    group: int
    author: int
    size: int
    month: int
    day: int
    time: int
    name: int


OptionColorLiteral = Literal["auto", "always", "never"]
OptionFormatLiteral = Literal[
    "across", "commas", "horizontal", "long", "single-column", "verbose", "vertical"
]

# Default Values
DEFAULT_MAX_WIDTHS: MaxWidths = {
    "perm": 13,
    "link": 3,
    "owner": 10,
    "group": 10,
    "author": 10,
    "size": 8,
    "month": 4,
    "day": 2,
    "time": 7,
    "name": 15,
}
DEFAULT_COLORS = {
    "default": "\033[0m",  # Reset
    "blue": "\033[34m",  # Directory
    "green": "\033[32m",  # Executable file
    "cyan": "\033[36m",  # Symbolic link
    "red": "\033[31m",  # Compressed file
    "magenta": "\033[35m",  # Image, FIFO, Socket
    "yellow": "\033[33m",  # Block/Character device
    "blinking_red": "\033[5;31m",  # Blinking red for broken symbolic link
}
DEFAULT_FULL_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class LS(CommandBase):

    filter_flags: set[str] = {
        # Filtering Options
        "-a",  # do not ignore entries starting with .
        "--all",  # do not igno# -rw-r--r--  1 hashedalgorithm hashedalgorithm   807 Mar 31  2024 .profilere entries starting with .
        "-A",  # do not list implied . and ..
        "--almost-all",  # do not list implied . and ..
        "--ignore-backups",  # do not list implied entries ending with ~
        "-B",  # do not list implied entries ending with ~
        "-f",  # same as -a -U
    }

    format_flags: set[str] = {
        # Formatting Options
        "-1",  # prints each item in 1 column
        "--author",  # with -l, print the author of each file
        "-b",  # print C-style escapes for nongraphic characters
        "--escape",  # print C-style escapes for nongraphic characters
        "--block-size",  # with -l, scale sizes by SIZE when printing them
        "-c",  # with -lt: sort by, and show, ctime; with -l: show ctime and sort by name; otherwise: sort by ctime, newest first
        "-C",  # list entries by columns
        "--color",  # color the output WHEN
        "-D",  # generate output designed for Emacs' dired mode
        "--dired",  # generate output designed for Emacs' dired mode
        "-F",  # append indicator (one of */=>@|) to entries WHEN
        "--classify",  # append indicator (one of */=>@|) to entries WHEN
        "--file-type",  # likewise, except do not append '*'
        "--format",  # set output format: across, commas, horizontal, long, single-column, verbose, vertical
        "--full-time",  # like -l --time-style=full-iso
        "-g",  # like -l, but do not list owner
        "-G",  # in a long listing, don't print group names
        "--no-group",  # in a long listing, don't print group names
        "-h",  # with -l and -s, print sizes like 1K 234M 2G etc.
        "--human-readable",  # with -l and -s, print sizes like 1K 234M 2G etc.
        "--si",  # likewise, but use powers of 1000 not 1024
        "-H",  # follow symbolic links listed on the command line
        "--dereference-command-line",  # follow symbolic links listed on the command line
        "--dereference-command-line-symlink-to-dir",  # follow each command line symbolic link that points to a directory
        "--hide",  # do not list implied entries matching shell PATTERN
        "--hyperlink",  # hyperlink file names WHEN
        "--indicator-style",  # append indicator with style WORD to entry names
        "-i",  # print the index number of each file
        "--inode",  # print the index number of each file
        "-I",  # do not list implied entries matching shell PATTERN
        "--ignore",  # do not list implied entries matching shell PATTERN
        "-k",  # default to 1024-byte blocks for file system usage
        "--kibibytes",  # default to 1024-byte blocks for file system usage
        "-l",  # use a long listing format
        "-L",  # show info for the file the link references rather than for the link itself
        "--dereference",  # show info for the file the link references rather than for the link itself
        "-m",  # fill width with a comma separated list of entries
        "-n",  # like -l, but list numeric user and group IDs
        "--numeric-uid-gid",  # like -l, but list numeric user and group IDs
        "-N",  # print entry names without quoting
        "--literal",  # print entry names without quoting
        "-o",  # like -l, but do not list group information
        "-p",  # append / indicator to directories
        "--indicator-style=slash",  # append / indicator to directories
        "-q",  # print ? instead of nongraphic characters
        "--hide-control-chars",  # print ? instead of nongraphic characters
        "--show-control-chars",  # show nongraphic characters as-is
        "-Q",  # enclose entry names in double quotes
        "--quote-name",  # enclose entry names in double quotes
        "--quoting-style",  # use quoting style WORD for entry names
        "-r",  # reverse order while sorting
        "--reverse",  # reverse order while sorting
        "-R",  # list subdirectories recursively
        "--recursive",  # list subdirectories recursively
        "-s",  # print the allocated size of each file, in blocks
        "--size",  # print the allocated size of each file, in blocks
        "-S",  # sort by file size, largest first
        "--sort",  # change default 'name' sort to WORD
        "--time",  # select which timestamp used to display or sort
        "--time-style",  # time/date format with -l
        "-t",  # sort by time, newest first
        "-T",  # assume tab stops at each COLS instead of 8
        "--tabsize",  # assume tab stops at each COLS instead of 8
        "-u",  # with -lt: sort by, and show, access time; with -l: show access time and sort by name; otherwise: sort by access time, newest first
        "-U",  # do not sort directory entries
        "-v",  # natural sort of (version) numbers within text
        "-w",  # set output width to COLS. 0 means no limit
        "--width",  # set output width to COLS. 0 means no limit
        "-x",  # list entries by lines instead of by columns
        "-X",  # sort alphabetically by entry extension
        "-Z",  # print any security context of each file
        "--context",  # print any security context of each file
        "--zero",  # end each output line with NUL, not newline
        "-1",  # list one file per line
    }

    sort_flags: set[str] = {
        "-c",  # with -lt: sort by, and show, ctime; with -l: show ctime and sort by name; otherwise: sort by ctime, newest first
        "--group-directories-first",  # group directories before files
    }

    other_flags: set[str] = {
        # Others
        "-d",  # list directories themselves, not their contents
        "--directory",  # list directories themselves, not their contents
        "--help",  # display this help and exit
        "--version",  # output version information and exit
    }

    def __init__(
        self, file_system: FileSystem, parsed: ParsedCommand, cwd: str
    ) -> None:
        super().__init__("ls", "9.4")
        self.file_system = file_system
        self.parsed = parsed
        self.cwd = cwd

    def print_entry(
        self,
        entry: File | Directory,
        max_widths: MaxWidths = DEFAULT_MAX_WIDTHS,
        _1: bool = False,
        _author: bool = False,
        _b: bool = False,
        _escape: bool = False,
        _block_size: str = "",
        _l: bool = False,
        _c: bool = False,
        _C: bool = False,  # TODO
        _color: OptionColorLiteral = "auto",
        _D: bool = False,
        _dired: bool = False,
        _F: bool = False,
        _classify: bool = False,
        _file_type: bool = False,
        _format: OptionFormatLiteral | None = None,
        _full_time: bool = False,
        _g: bool = False,
        _G: bool = False,
        _no_group=False,
        _h: bool = False,
        _human_readable: bool = False,
        _si: bool = False,
        _t: bool = False,
    ):
        formatter = Formatter()

        name = formatter._b(entry.name) if _b or _escape else entry.name
        name = formatter.colorize(
            name,
            "dir" if isinstance(entry, Directory) else entry.extension,
            True if _color == "never" else False,
        )
        if _F or _classify:
            name = formatter._F(name, entry.extension, _file_type)

        size = (
            formatter._block_size(entry.size, _block_size)
            if _block_size
            else entry.size
        )

        time = entry.created_time.utcnow() if _full_time else entry.get_created_time()
        if _l and _c:
            time = entry.ctime.utcnow() if _full_time else entry.get_ctime()
        elif _l and _t:
            time = entry.mtime.utcnow() if _full_time else entry.get_mtime()

        if _D or _dired:
            max_widths = {
                "perm": DEFAULT_MAX_WIDTHS.get("perm") + 2,
                "link": DEFAULT_MAX_WIDTHS.get("link") + 1,
                "owner": DEFAULT_MAX_WIDTHS.get("owner") + 2,
                "group": DEFAULT_MAX_WIDTHS.get("group") + 2,
                "author": DEFAULT_MAX_WIDTHS.get("author") + 2,
                "size": DEFAULT_MAX_WIDTHS.get("size") + 2,
                "month": DEFAULT_MAX_WIDTHS.get("month") + 2,
                "day": DEFAULT_MAX_WIDTHS.get("day") + 1,
                "time": DEFAULT_MAX_WIDTHS.get("time") + 2,
                "name": DEFAULT_MAX_WIDTHS.get("name") + 2,
            }

        if _full_time:
            max_widths["time"] = 28

        if _h or _human_readable:
            max_widths["size"] = 8
            size = formatter._h(entry.size)

        if _si:
            max_widths["size"] = 8
            size = formatter._h(entry.size, 1000)

        link_count = entry.get_link()

        if _l or _format == "long" or _format == "verbose":
            _fperm = f"{entry.perm:<{max_widths.get("perm")}}"
            _flink_count = f"{link_count:<{max_widths.get("link")}}"
            _fowner = f"{entry.owner:<{max_widths.get("owner")}}" if not _g else ""
            _fgroup = (
                f"{entry.group:<{max_widths.get("author")}}"
                if not _G and not _no_group
                else ""
            )
            _fauthor = (
                f"{f"{entry.owner:<{max_widths.get("owner")}}" if _author else ""}"
            )
            _fsize = f"{str(size):<{max_widths.get("size")}}"
            _fmonth = f"{entry.get_created_month():<{max_widths.get("month")}}"
            _fday = f"{entry.get_created_day():<{max_widths.get("day")}}"
            _ftime = f"{str(time):<{max_widths.get("time")}}"
            _fname = f"{name:<{max_widths.get("name")}}"

            owner_metadata = f"{_fowner}{_fgroup}{_fauthor}"
            time_metadata = (
                f"{f"{_fmonth}{_fday}{_ftime}" if not _full_time else _ftime}"
            )

            return f"{_fperm}{_flink_count}{owner_metadata}{_fsize}{time_metadata}{_fname}\n"
        elif _format == "commas":
            return f"{_fname},"
        elif _format == "single-column":
            return f"{_fname}\n"
        else:
            return f"{_fname}\t"

    def _no_args(self):
        output = ""
        for child in self.file_system.cwd.children.values():
            output = (
                output
                + f"{self.print_entry(
                child,
            )}\t"
            )

        return output

    def filter(self, directory: Directory) -> list[Directory | File]:
        filtered_args = self.parsed.group(["flag"], self.filter_flags)

        if filtered_args.__len__() == 0:
            return list(
                filter(
                    lambda child: not child.name.startswith("."),
                    directory.children.values(),
                )
            )

        filtered_entries: list[Directory | File] = []

        for child in directory.children.values():

            atleast_one: bool = False
            for arg in filtered_args:
                if arg.name == "-a" or arg.name == "-all" or arg.name == "-f":
                    atleast_one = True
                    continue
                if arg.name == "-A" or arg.name == "--almost-all":
                    if not child.name.startswith("."):
                        atleast_one = True
                    continue
                if arg.name == "--ignore-backups" or arg.name == "-B":
                    if not child.name.endswith("~"):
                        atleast_one = True
                    continue

            if atleast_one:
                filtered_entries.append(child)

        return filtered_entries

    def format(self, filtered_entries: list[Directory]) -> list[str]:
        output = ""
        filtered_args = self.parsed.group(
            ["flag", "positional", "option"], self.format_flags
        )

        is_long = self.parsed.find("-l") or (
            self.parsed.find("--format")
            and self.parsed.find("--format").value in ["verbose", "long"]
        )

        max_widths: MaxWidths = {
            "perm": max(len(entry.perm) for entry in filtered_entries) + 2,
            "link": max(len(str(entry.get_link())) for entry in filtered_entries) + 1,
            "owner": max(len(entry.owner) for entry in filtered_entries) + 2,
            "group": max(len(entry.group) for entry in filtered_entries) + 2,
            "author": max(len(entry.owner) for entry in filtered_entries) + 2,
            "size": max(len(str(entry.size)) for entry in filtered_entries) + 2,
            "month": max(len(entry.get_created_month()) for entry in filtered_entries)
            + 2,
            "day": max(len(str(entry.get_created_day())) for entry in filtered_entries)
            + 2,
            "time": max(len(entry.get_created_time()) for entry in filtered_entries)
            + 2,
            "name": max(len(entry.name) for entry in filtered_entries) + 2,
        }

        if filtered_args.__len__() == 0:
            return []

        if is_long:
            output = output + (
                f"{self.calculate_block_size([entry.size for entry in filtered_entries])}\n"
            )

        for entry in filtered_entries:

            output = output + self.print_entry(
                entry=entry,
                max_widths=max_widths,
                _1=False,
                _author=self.parsed.find("--author"),
                _b=self.parsed.find("-b"),
                _escape=self.parsed.find("--escape"),
                _c=self.parsed.find("-c"),
                _C=self.parsed.find("-C"),
                _l=self.parsed.find("-l"),
                _F=self.parsed.find("-F"),
                _classify=self.parsed.find("--classify"),
                _format=self.parsed.find("--format"),
                _full_time=self.parsed.find("--full-time"),
                _g=self.parsed.find("-g"),
                _G=self.parsed.find("-G"),
                _no_group=self.parsed.find("--no-group"),
                _human_readable=self.parsed.find("--human-readable"),
                _h=self.parsed.find("-h"),
                _si=self.parsed.find("--si"),
            )

        return output

    def calculate_block_size(self, file_sizes: list[int], block_size: int = 512) -> int:
        """
        Calculates the total block size used by a list of files.

        Args:
            file_sizes (list[int]): A list of file sizes in bytes.
            block_size (int): The size of a single block in bytes (default is 512).

        Returns:
            int: The total number of blocks used by the files.
        """
        total_blocks = 0

        for size in file_sizes:
            # Calculate the number of blocks required for each file
            blocks = (size + block_size - 1) // block_size  # Ceiling division
            total_blocks += blocks

        return f"total {total_blocks}"

    def run(self) -> str | None:
        output: list[str] = []

        if self.parsed.args.__len__() == 0:
            return self._no_args()

        if self.parsed.find("--help"):
            return self.get_help()

        if self.parsed.find("--version"):
            return self.get_version()

        positional_args = self.parsed.group(["positional"], {})
        source_paths = [self.cwd if positional_args.__len__() == 0 else positional_args]

        is_multiple_source: bool = source_paths.__len__() > 1

        for source_path in source_paths:
            directory = self.file_system.get_directory(source_path)

            filtered_entries = self.filter(directory)
            output.append(self.format(filtered_entries))

        return self.print(output)

    def get_version(self):
        return f"""
ls (GNU coreutils) {self.version}
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Richard M. Stallman and David MacKenzie.

    """

    def help(self):
        return """ 
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
-a, --all                  do not ignore entries starting with .
-A, --almost-all           do not list implied . and ..
    --author               with -l, print the author of each file
-b, --escape               print C-style escapes for nongraphic characters
    --block-size=SIZE      with -l, scale sizes by SIZE when printing them;
                            e.g., '--block-size=M'; see SIZE format below

-B, --ignore-backups       do not list implied entries ending with ~
-c                         with -lt: sort by, and show, ctime (time of last
                            change of file status information);
                            with -l: show ctime and sort by name;
                            otherwise: sort by ctime, newest first

-C                         list entries by columns
    --color[=WHEN]         color the output WHEN; more info below
-d, --directory            list directories themselves, not their contents
-D, --dired                generate output designed for Emacs' dired mode
-f                         list all entries in directory order
-F, --classify[=WHEN]      append indicator (one of */=>@|) to entries WHEN
    --file-type            likewise, except do not append '*'
    --format=WORD          across -x, commas -m, horizontal -x, long -l,
                            single-column -1, verbose -l, vertical -C

    --full-time            like -l --time-style=full-iso
-g                         like -l, but do not list owner
    --group-directories-first
                            group directories before files;
                            can be augmented with a --sort option, but any
                            use of --sort=none (-U) disables grouping

-G, --no-group             in a long listing, don't print group names
-h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.
    --si                   likewise, but use powers of 1000 not 1024
-H, --dereference-command-line
                            follow symbolic links listed on the command line
    --dereference-command-line-symlink-to-dir
                            follow each command line symbolic link
                            that points to a directory

    --hide=PATTERN         do not list implied entries matching shell PATTERN
                            (overridden by -a or -A)

    --hyperlink[=WHEN]     hyperlink file names WHEN
    --indicator-style=WORD
                            append indicator with style WORD to entry names:
                            none (default), slash (-p),
                            file-type (--file-type), classify (-F)

-i, --inode                print the index number of each file
-I, --ignore=PATTERN       do not list implied entries matching shell PATTERN
-k, --kibibytes            default to 1024-byte blocks for file system usage;
                            used only with -s and per directory totals

-l                         use a long listing format
-L, --dereference          when showing file information for a symbolic
                            link, show information for the file the link
                            references rather than for the link itself

-m                         fill width with a comma separated list of entries
-n, --numeric-uid-gid      like -l, but list numeric user and group IDs
-N, --literal              print entry names without quoting
-o                         like -l, but do not list group information
-p, --indicator-style=slash
                            append / indicator to directories
-q, --hide-control-chars   print ? instead of nongraphic characters
    --show-control-chars   show nongraphic characters as-is (the default,
                            unless program is 'ls' and output is a terminal)

-Q, --quote-name           enclose entry names in double quotes
    --quoting-style=WORD   use quoting style WORD for entry names:
                            literal, locale, shell, shell-always,
                            shell-escape, shell-escape-always, c, escape
                            (overrides QUOTING_STYLE environment variable)

-r, --reverse              reverse order while sorting
-R, --recursive            list subdirectories recursively
-s, --size                 print the allocated size of each file, in blocks
-S                         sort by file size, largest first
    --sort=WORD            sort by WORD instead of name: none (-U), size (-S),
                            time (-t), version (-v), extension (-X), width

    --time=WORD            select which timestamp used to display or sort;
                            access time (-u): atime, access, use;
                            metadata change time (-c): ctime, status;
                            modified time (default): mtime, modification;
                            birth time: birth, creation;
                            with -l, WORD determines which time to show;
                            with --sort=time, sort by WORD (newest first)

    --time-style=TIME_STYLE
                            time/date format with -l; see TIME_STYLE below
-t                         sort by time, newest first; see --time
-T, --tabsize=COLS         assume tab stops at each COLS instead of 8
-u                         with -lt: sort by, and show, access time;
                            with -l: show access time and sort by name;
                            otherwise: sort by access time, newest first

-U                         do not sort; list entries in directory order
-v                         natural sort of (version) numbers within text
-w, --width=COLS           set output width to COLS.  0 means no limit
-x                         list entries by lines instead of by columns
-X                         sort alphabetically by entry extension
-Z, --context              print any security context of each file
    --zero                 end each output line with NUL, not newline
-1                         list one file per line
    --help        display this help and exit
    --version     output version information and exit

The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
Units are K,M,G,T,P,E,Z,Y,R,Q (powers of 1024) or KB,MB,... (powers of 1000).
Binary prefixes can be used, too: KiB=K, MiB=M, and so on.

The TIME_STYLE argument can be full-iso, long-iso, iso, locale, or +FORMAT.
FORMAT is interpreted like in date(1).  If FORMAT is FORMAT1<newline>FORMAT2,
then FORMAT1 applies to non-recent files and FORMAT2 to recent files.
TIME_STYLE prefixed with 'posix-' takes effect only outside the POSIX locale.
Also the TIME_STYLE environment variable sets the default style to use.

The WHEN argument defaults to 'always' and can also be 'auto' or 'never'.

Using color to distinguish file types is disabled both by default and
with --color=never.  With --color=auto, ls emits color codes only when
standard output is connected to a terminal.  The LS_COLORS environment
variable can change the settings.  Use the dircolors(1) command to set it.

Exit status:
0  if OK,
1  if minor problems (e.g., cannot access subdirectory),
2  if serious trouble (e.g., cannot access command-line argument).

GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
Full documentation <https://www.gnu.org/software/coreutils/ls>
or available locally via: info '(coreutils) ls invocation'
        """


class Formatter:

    executable = [".sh", ".exe", ".bin", ".out", ".py", ".java", ".dmg"]
    compressed = [".tar", ".gz", ".zip", ".rar", ".7z"]
    images = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
    pipe = [".fifo", ".pipe"]
    socket = [".socket"]
    other = [".sda", ".tty"]
    symlink = ["symlink"]
    broken_symlink = ["broken_symlink"]

    def __init__(self):
        pass

    def _b(input: str) -> str:
        """
        Finds and replaces non-graphic characters and special Unicode characters
        in a string with their corresponding escape sequences.

        Args:
            input_string (str): The input string to process.

        Returns:
            str: The string with non-graphic and special characters replaced by escape sequences.
        """
        escape_map = {
            " ": r"\ ",  # Space
            "\t": r"\t",  # Tab
            "\n": r"\n",  # Newline
            "\r": r"\r",  # Carriage return
            "\v": r"\v",  # Vertical tab
            "\f": r"\f",  # Form feed
        }

        escaped_string = ""
        for char in input:
            if char in escape_map:
                escaped_string += escape_map[char]
            elif ord(char) < 32 or ord(char) == 127:  # Non-printable ASCII
                escaped_string += f"\\x{ord(char):02x}"
            elif ord(char) > 127:  # Non-ASCII characters (e.g., Unicode)
                for byte in char.encode("utf-8"):
                    escaped_string += f"\\x{byte:02x}"
            else:
                escaped_string += char

        return escaped_string

    def _block_size(size_in_bytes: int, block_size: str) -> str:
        """
        Converts a size in bytes to a specified block size format, similar to the
        behavior of the `--block-size` flag in the `ls` command.

        Args:
            size_in_bytes (int): The size in bytes to be converted.
            block_size (str): The block size format. Can be one of:
                                "K", "M", "G", "T", "P", "E" (powers of 1024),
                                "KB", "MB", "GB", "TB", "PB", "EB" (powers of 1000),
                                or a custom block size (e.g., "512").

        Returns:
            str: The converted size as a formatted string.

        Raises:
            ValueError: If the block size format is invalid.
        """
        # Define conversion factors for powers of 1024
        power_of_1024 = {
            "K": 1024,
            "M": 1024**2,
            "G": 1024**3,
            "T": 1024**4,
            "P": 1024**5,
            "E": 1024**6,
        }

        # Define conversion factors for powers of 1000
        power_of_1000 = {
            "KB": 1000,
            "MB": 1000**2,
            "GB": 1000**3,
            "TB": 1000**4,
            "PB": 1000**5,
            "EB": 1000**6,
        }

        # Check if the block size is a power of 1024
        if block_size in power_of_1024:
            converted_size = size_in_bytes / power_of_1024[block_size]
            return f"{converted_size:.2f} {block_size}"

        # Check if the block size is a power of 1000
        elif block_size in power_of_1000:
            converted_size = size_in_bytes / power_of_1000[block_size]
            return f"{converted_size:.2f} {block_size}"

        # Check if the block size is a custom numeric value
        elif block_size.isdigit():
            block_size_value = int(block_size)
            converted_size = size_in_bytes / block_size_value
            return f"{converted_size:.2f} (blocks of {block_size} bytes)"

        # If the block size format is invalid, raise an error
        else:
            raise ValueError(
                f"Invalid block size format '{block_size}'. Must be one of: "
                f"{', '.join(power_of_1024.keys())}, {', '.join(power_of_1000.keys())}, or a numeric value."
            )

    def colorize(self, file_name: str, file_extension: str, is_neutral: bool) -> str:
        """
        Returns a color-formatted string based on the file type.

        Args:
            file_name (str): The name of the file.
            file_extension (str): The extension of the file (e.g., '.txt', '.png').

        Returns:
            str: The file name wrapped in the appropriate color code.
        """
        if is_neutral:
            return f"\033[0m{file_name}\033[0m"

        # Determine the color based on file type
        if file_extension in self.executable:
            color = DEFAULT_COLORS["green"]  # Executable file
        elif file_extension in self.compressed:
            color = DEFAULT_COLORS["red"]  # Compressed file
        elif file_extension in self.images:
            color = DEFAULT_COLORS["magenta"]  # Image file
        elif file_extension in self.pipe:
            color = DEFAULT_COLORS["magenta"]  # FIFO (named pipe)
        elif file_extension in self.socket:
            color = DEFAULT_COLORS["magenta"]  # Socket
        elif file_extension in self.other:
            color = DEFAULT_COLORS["yellow"]  # Block/Character device
        elif file_extension in self.symlink:
            color = DEFAULT_COLORS["cyan"]  # Symbolic link
        elif file_extension in self.broken_symlink:
            color = DEFAULT_COLORS["blinking_red"]  # Broken symbolic link
        elif file_extension == "dir":
            color = DEFAULT_COLORS["blue"]  # Directory
        else:
            color = DEFAULT_COLORS["default"]  # Regular file or unknown type

        # Return the color-formatted string
        return f"\033[1m{color}{file_name}\033[0m"

    def _F(self, name: str, extension: str, file_type: bool) -> str:
        """
        Modifies a folder/file name by appending a specific character based on its type.

        Args:
            name (str): The name of the folder or file (without extension).
            extension (str): The file extension (e.g., "txt", "sh", "py").

        Returns:
            str: The modified name with an appended character.
        """

        if extension == "dir":
            append_char = "/"
        elif extension in self.executable:
            append_char = "*"
        elif extension in self.executable:
            append_char = "="  # Compressed file
        elif extension in self.pipe:
            append_char = "|"  # FIFO (named pipe)
        elif extension in self.socket:
            append_char = "="  # Socket
        elif extension in self.symlink:
            append_char = "@"  # Symbolic link

        else:
            append_char = ""  # Regular file or unknown type

        # Return the modified name
        return f"{name}{append_char}"

    def _h(self, size: int, power: int = 1024) -> str:
        """
        Converts a size in bytes to a human-readable format (e.g., KB, MB, GB).

        Args:
            size_in_bytes (int): The size in bytes.

        Returns:
            str: The size in a human-readable format with appropriate units.
        """
        # Define the units and their corresponding thresholds
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
        size = float(size)  # Convert to float for division

        # Iterate through the units, dividing the size until it's less than 1024
        for unit in units:
            if size < power:
                return f"{size:.1f} {unit}"  # Format with 1 decimal place
            size /= power  # Divide by power to move to the next unit

        # If the size is extremely large, return it in the largest unit (EB)
        return f"{size:.1f} {units[-1]}"
