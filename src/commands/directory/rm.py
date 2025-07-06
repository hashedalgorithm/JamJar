# rm.py
from models.file_system import FileSystem, Directory
from utils.parser import ParsedCommand, ParsedArgument
from commands.base import CommandBase

class RM(CommandBase):
    def __init__(self, file_system: FileSystem, parsed: ParsedCommand) -> None:
        super().__init__("rm")
        self.file_system = file_system
        self.parsed = parsed

    def run(self) -> str | None:
        flags = set()
        files = []

        for arg in self.parsed.args:
            if arg.type == "flag":
                flags.add(arg.name)
            elif arg.type == "positional":
                files.append(arg.value)

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
                "  -r, -R, --recursive   remove directories and their contents recursively\n"
                "  -d, --dir             remove empty directories\n"
                "  -v, --verbose         explain what is being done\n"
                "      --help            display this help and exit\n"
                "      --version         output version information and exit\n"
            )

        recursive = "-r" in flags or "-R" in flags or "--recursive" in flags
        force = "-f" in flags or "--force" in flags
        verbose = "-v" in flags or "--verbose" in flags
        dir_only = "-d" in flags or "--dir" in flags

        outputs = []

        for name in files:
            target = self.file_system.cwd.children.get(name)
            if not target:
                if not force:
                    outputs.append(f"rm: cannot remove '{name}': No such file or directory")
                continue

            if isinstance(target, Directory):
                if dir_only:
                    if target.children:
                        outputs.append(f"rm: cannot remove '{name}': Directory not empty")
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

# ---------- Inline test harness ----------

if __name__ == "__rm__":
    # Minimal mock implementations for testing

    class Directory:
        def __init__(self, name):
            self.name = name
            self.children = {}
            self.parent = None

        def add_child(self, child):
            self.children[child.name] = child
            child.parent = self

        def __repr__(self):
            return f"Directory({self.name})"

    class File:
        def __init__(self, name):
            self.name = name

    class FileSystem:
        def __init__(self):
            self.root = Directory("root")
            self.cwd = self.root
            self.path_stack = ["root"]

    class ParsedArgument:
        def __init__(self, type, value=None, name=None):
            self.type = type
            self.value = value
            self.name = name

    class ParsedCommand:
        def __init__(self, command, args):
            self.command = command
            self.args = args

    # Set up virtual file system
    fs = FileSystem()
    docs = Directory("docs")
    file1 = File("note.txt")
    file2 = File("log.txt")
    empty_dir = Directory("empty")
    non_empty_dir = Directory("nonempty")
    child_file = File("inside.txt")

    non_empty_dir.add_child(child_file)
    fs.cwd.add_child(docs)
    fs.cwd.add_child(file1)
    fs.cwd.add_child(file2)
    fs.cwd.add_child(empty_dir)
    fs.cwd.add_child(non_empty_dir)

    def build_parsed(cmd, args):
        parsed_args = []
        for arg in args:
            if arg.startswith("-"):
                parsed_args.append(ParsedArgument(type="flag", name=arg))
            else:
                parsed_args.append(ParsedArgument(type="positional", value=arg))
        return ParsedCommand(command=cmd, args=parsed_args)

    tests = [
        ["rm", ["note.txt"]],
        ["rm", ["-v", "log.txt"]],
        ["rm", ["-d", "empty"]],
        ["rm", ["-d", "nonempty"]],
        ["rm", ["-r", "nonempty"]],
        ["rm", ["nonexistent"]],
        ["rm", ["-f", "nonexistent"]],
        ["rm", ["--help"]],
        ["rm", ["--version"]],
    ]

    for cmd, args in tests:
        parsed = build_parsed(cmd, args)
        rm = RM(fs, parsed)
        result = rm.run()
        print(f"Command: {' '.join(args)}")
        if result:
            print(result)
        else:
            print("Success with no output.")
        print("-" * 40)
