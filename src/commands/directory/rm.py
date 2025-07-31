# rm.py
from models.file_system import FileSystem, Directory
from utils.parser import ParsedCommand, ParsedArgument
from commands.base import CommandBase
from models.terminals import Terminal


class RM(CommandBase):
    def __init__(
        self, file_system: FileSystem, parsed: ParsedCommand, terminal=Terminal
    ) -> None:
        super().__init__("rm", "9.4")
        self.file_system = file_system
        self.parsed = parsed
        self.terminal = terminal

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
            return self.get_version()

        if "--help" in flags:
            return self.get_help()

        recursive = "-r" in flags or "-R" in flags or "--recursive" in flags
        force = "-f" in flags or "--force" in flags
        verbose = "-v" in flags or "--verbose" in flags
        dir_only = "-d" in flags or "--dir" in flags

        outputs = []

        for name in files:
            target_directory = self.file_system.get_directory(self.terminal.cwd)
            if target_directory is None:
                outputs.append(f"rm: cannot remove '{name}': No such file or directory")
                continue

            target = target_directory.children.get(name)
            if not target:
                if not force:
                    outputs.append(
                        f"rm: cannot remove '{name}': No such file or directory"
                    )
                continue

            if isinstance(target, Directory):
                if dir_only:
                    if target.children:
                        outputs.append(
                            f"rm: cannot remove '{name}': Directory not empty"
                        )
                        continue
                    del target_directory.children[name]
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
                del target_directory.children[name]
                if verbose:
                    outputs.append(f"removed '{name}'")

        return "\n".join(outputs) if outputs else None
