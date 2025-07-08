from models.file_system import FileSystem, Directory, File
from utils.parser import ParsedCommand, ParsedArgument
from commands.base import CommandBase
from utils.parser import CommandParser

class RM(CommandBase):
    def __init__(self, file_system: FileSystem, parsed: ParsedCommand) -> None:
        super().__init__("rm")
        self.file_system = file_system
        self.parsed = parsed

    def resolve_path(self, path: str) -> Directory | File | None:
        parser = CommandParser()
        parts = parser.split_path(path)
        # Start node depends on absolute or relative path
        if parts and parts[0] == "/":
            node = self.file_system.root
            parts = parts[1:]  # remove root "/" from parts
        else:
            node = self.file_system.cwd

        # Use a stack to simulate navigation for ".." and "."
        stack = []

        # For absolute path start stack empty, for relative start with cwd path stack
        if path.startswith("/"):
            # absolute path, start fresh stack from root
            stack = []
        else:
            # relative path, start from current working directory path stack (copy)
            stack = list(self.file_system.path_stack)

        for part in parts:
            if part in ("", "."):
                continue
            elif part == "..":
                if stack and stack[-1] != "root":  # don't go above root
                    stack.pop()
            else:
                stack.append(part)

        # Now walk down from root following stack to find target node
        current = self.file_system.root
        for part in stack[1:]:  # skip "root" which is at index 0
            if isinstance(current, Directory) and part in current.children:
                current = current.children[part]
            else:
                return None
        return current

    def run(self) -> str | None:
        flags = set()
        files = []

        for arg in self.parsed.args:
            if arg.type == "flag":
                flags.add(arg.name)
            elif arg.type == "positional":
                files.append(arg.value)

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

        if not files:
            return "rm: missing operand\nTry 'rm --help' for more information."

        recursive = "-r" in flags or "-R" in flags or "--recursive" in flags
        force = "-f" in flags or "--force" in flags
        verbose = "-v" in flags or "--verbose" in flags
        dir_only = "-d" in flags or "--dir" in flags

        outputs = []

        def recursive_delete(node: Directory, path: str):
            """Recursively delete contents of a directory"""
            for child_name in list(node.children.keys()):
                child = node.children[child_name]
                full_path = f"{path}/{child_name}"
                if isinstance(child, Directory):
                    recursive_delete(child, full_path)
                else:
                    del node.children[child_name]
                    if verbose:
                        outputs.append(f"removed '{full_path}'")
            node.children.clear()

        for path_str in files:
            target = self.resolve_path(path_str)
            if not target:
                if not force:
                    outputs.append(f"rm: cannot remove '{path_str}': No such file or directory")
                continue

            # Determine the parent directory to remove the target from
            # We must remove target from its parent's children dict
            # So resolve parent node
            parent_path = "/".join(path_str.split("/")[:-1])
            parent_node = self.file_system.cwd if parent_path == "" else self.resolve_path(parent_path)
            if parent_node is None or not isinstance(parent_node, Directory):
                if not force:
                    outputs.append(f"rm: cannot remove '{path_str}': No such file or directory")
                continue

            name = path_str.split("/")[-1]

            if isinstance(target, Directory):
                if dir_only:
                    if target.children:
                        outputs.append(f"rm: cannot remove '{path_str}': Directory not empty")
                        continue
                    del parent_node.children[name]
                    if verbose:
                        outputs.append(f"removed directory: '{path_str}'")
                elif recursive:
                    recursive_delete(target, path_str)
                    del parent_node.children[name]
                    if verbose:
                        outputs.append(f"removed directory: '{path_str}'")
                else:
                    outputs.append(f"rm: cannot remove '{path_str}': Is a directory")
            else:
                if dir_only:
                    outputs.append(f"rm: cannot remove '{path_str}': Not a directory")
                    continue
                if recursive:
                    outputs.append(f"rm: cannot remove '{path_str}': Not a directory")
                    continue
                del parent_node.children[name]
                if verbose:
                    outputs.append(f"removed '{path_str}'")

        return "\n".join(outputs) if outputs else None
