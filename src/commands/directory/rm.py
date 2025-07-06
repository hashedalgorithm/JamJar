from models.file_system import FileSystem
from models.directory import Directory
from ..base import CommandBase
from utils.parser import CommandParser, ParsedCommand


class RMFlagMap:
    def __init__(
        self,
        f=False,
        i=False,
        r=False,
        d=False,
        v=False,
        one_file_system=False,
        no_preserve_root=False,
        preserve_root=False,
    ):
        self.f = f  # force
        self.i = i  # interactive
        self.r = r  # recursive
        self.d = d  # directory
        self.v = v  # verbose
        self.one_file_system = one_file_system  # one file system
        self.no_preserve_root = no_preserve_root  # no preserve root
        self.preserve_root = preserve_root  # preserve root

    def set_flag(self, flag: str, value: bool) -> None:
        if hasattr(self, flag):
            setattr(self, flag, value)


class RM(CommandBase):
    def __init__(self, file_system: FileSystem, parsed: ParsedCommand, args: list[str]):
        super().__init__("rm")
        self.parsed = parsed
        self.args = args
        self.file_system = file_system
        self.flags = self.extract_flags(args)
        self.paths = self.extract_paths(args)
        self.flag_map = self.initialize_flag_map(self.flags)

    def initialize_flag_map(self, flags: list[str]) -> RMFlagMap:
        """
        Initialize the flag map based on the provided flags.
        """
        flag_map = RMFlagMap()
        for flag in flags:
            if flag == "-f":
                flag_map.f = True
            elif flag == "-i" | "--interactive":
                flag_map.i = True
            elif flag in "-r" | "-R" | "--recursive":
                flag_map.r = True
            elif flag == "-d" | "--dir":
                flag_map.d = True
            elif flag == "-v":
                flag_map.v = True
            elif flag == "--one-file-system":
                flag_map.one_file_system = True
            elif flag == "--no-preserve-root":
                flag_map.no_preserve_root = True
            elif flag == "--preserve-root":
                flag_map.preserve_root = True

        return flag_map

    def run(self, args: list[str]) -> str | None:
        flags = self.extract_flags(args)
        paths = self.extract_paths(args)

        # Handle --version and --help
        if "--version" in flags:
            return (
                "rm (GNU coreutils) 9.4\n"
                "Copyright (C) 2023 Free Software Foundation, Inc.\n"
                "License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.\n"
                "This is free software: you are free to change and redistribute it.\n"
                "There is NO WARRANTY, to the extent permitted by law.\n\n"
                "Written by Paul Rubin, David MacKenzie, Richard M. Stallman,\n"
                "and Jim Meyering.\n"
            )
        if "--help" in flags:
            return (
                "Usage: rm [OPTION]... [FILE]...\n"
                "Remove (unlink) the FILE(s).\n\n"
                "  -f, --force           ignore nonexistent files and arguments, never prompt\n"
                "  -I                    prompt once before removing more than three files, or\n"
                "                          when removing recursively; less intrusive than -i,\n"
                "                          while still giving protection against most mistakes\n"
                "      --interactive[=WHEN]  prompt according to WHEN: never, once (-I), or\n"
                "                          always (-i); without WHEN, prompt always\n"
                "      --one-file-system  when removing a hierarchy recursively, skip any\n"
                "                          directory that is on a file system different from\n"
                "                          that of the corresponding command line argument\n"
                "      --no-preserve-root  do not treat '/' specially\n"
                "      --preserve-root[=all]  do not remove '/' (default);\n"
                "                              with 'all', reject any command line argument\n"
                "                              on a separate device from its parent\n"
                "  -r, -R, --recursive   remove directories and their contents recursively\n"
                "  -d, --dir             remove empty directories\n"
                "  -v, --verbose         explain what is being done\n"
                "      --help        display this help and exit\n"
                "      --version     output version information and exit\n\n"
                "By default, rm does not remove directories.  Use the --recursive (-r or -R)\n"
                "option to remove each listed directory, too, along with all of its contents.\n\n"
                "To remove a file whose name starts with a '-', for example '-foo',\n"
                "use one of these commands:\n"
                "  rm -- -foo\n"
                "  rm ./-foo\n\n"
                "Note that if you use rm to remove a file, it might be possible to recover\n"
                "some of its contents, given sufficient expertise and/or time.  For greater\n"
                "assurance that the contents are truly unrecoverable, consider using shred(1).\n\n"
                "GNU coreutils online help: <https://www.gnu.org/software/coreutils/>\n"
                "Full documentation <https://www.gnu.org/software/coreutils/rm>\n"
                "or available locally via: info '(coreutils) rm invocation'\n"
            )

    def rm(self, args):
        # For this example, we always work in 'a' folder

        flags = [arg for arg in args if arg.startswith("-")]
        files = [arg for arg in args if not arg.startswith("-")]

        recursive = any("r" in flag for flag in flags)
        force = any("f" in flag for flag in flags)
        verbose = any("v" in flag for flag in flags)
        dir_only = any("d" in flag for flag in flags)

        outputs = []

        for name in files:
            target = self.file_system.cwd.children.get(name)
            if not target:
                if not force:
                    outputs.append(
                        f"rm: cannot remove '{name}': No such file or directory"
                    )
                continue

            if isinstance(target, Directory):
                if dir_only:
                    # Only remove if directory is empty
                    if target.children:
                        outputs.append(
                            f"rm: cannot remove '{name}': Directory not empty"
                        )
                        continue
                    del self.file_system.cwd.children[name]
                    if verbose:
                        outputs.append(f"removed directory: '{name}'")
                elif recursive:
                    del self.file_system.cwd.children[name]
                    if verbose:
                        outputs.append(f"removed directory: '{name}'")
                else:
                    outputs.append(f"rm: cannot remove '{name}': Is a directory")
            else:
                if dir_only:
                    outputs.append(f"rm: cannot remove '{name}': Not a directory")
                    continue
                del self.file_system.cwd.children[name]
                if verbose:
                    outputs.append(f"removed '{name}'")

        return "\n".join(outputs) if outputs else None
