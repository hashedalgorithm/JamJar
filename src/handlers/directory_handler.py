from models.file_system import FileSystem
from utils.logger import Logger
from utils.parser import CommandParser
from models.terminals import Terminal

from commands.directory.cd import CD
from commands.directory.cp import CP
from commands.directory.ls import LS
from commands.directory.mkdir import MKDIR
from commands.directory.mv import MV
from commands.directory.rm import RM
from commands.directory.rmdir import RMDIR


class DirectoryHandler(Logger):
    def __init__(self, file_system: FileSystem) -> None:
        super().__init__()
        self.file_system = file_system
        self.parser = CommandParser()
        self.command_options_map = {
            "cd": [],
            "cp": [
                "--backup",
                "--block-size",
                "-S",
                "--suffix",
                "-t",
                "--target-directory",
                "--no-preserve",
                "--preserve",
                "--reflink",
                "--sparse",
                "--update",
                "--context",
            ],
            "ls": [
                "--block-size",
                "--color",
                "-F",
                "--classify",
                "--format",
                "--hide",
                "--hyperlink",
                "-p",
                "--indicator-style",
                "-I",
                "--ignore",
                "--quoting-style",
                "--sort",
                "--time",
                "--time-style",
                "-T",
                "--tabsize",
                "-w",
                "--width",
            ],
            "mkdir": ["-m", "--mode", "--context"],
            "mv": [
                "--backup",
                "-S",
                "--suffix",
                "-t",
                "--target-directory",
                "--update",
            ],
            "rm": ["--interactive"],
            "rmdir": [],
        }

    def handle(self, command: str, full_command: str, terminal: Terminal) -> str | None:
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)
        match command:
            case "cd":
                cd = CD(self.file_system, parsed)
                return cd.run()

            case "cp":
                cp = CP(self.file_system, parsed)
                return cp.run()

            case "ls":
                ls = LS(file_system=self.file_system, parsed=parsed, cwd=terminal.cwd)
                return ls.run()

            case "mkdir":
                mkdir = MKDIR(self.file_system, parsed)
                return mkdir.run()

            case "mv":
                mv = MV(self.file_system, parsed)
                return mv.run()

            case "rm":
                rm = RM(self.file_system, parsed)
                return rm.run()

            case "rmdir":
                rmdir = RMDIR(self.file_system, parsed)
                return rmdir.run()

            case _:
                self.logger.error(
                    f"Command '{command}' not recognized by DirectoryHandler."
                )
                return None
