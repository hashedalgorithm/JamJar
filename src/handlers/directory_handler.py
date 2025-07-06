from models.file_system import FileSystem
from utils.logger import Logger
from utils.parser import CommandParser

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

    def handle(self, command: str, full_command: str) -> str | None:
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)
        match command:
            case "cd":
                cd = CD(self.file_system)
                return cd.run(parsed)

            case "cp":
                cp = CP(self.file_system)
                return cp.run(parsed)

            case "ls":
                ls = LS(self.file_system)
                return ls.run(parsed)

            case "mkdir":
                mkdir = MKDIR(self.file_system)
                return mkdir.run(parsed)

            case "mv":
                mv = MV(self.file_system)
                return mv.run(parsed)

            case "rm":
                rm = RM(self.file_system)
                return rm.run(parsed)

            case "rmdir":
                rmdir = RMDIR(self.file_system)
                return rmdir.run(parsed)

            case _:
                print(f"Command '{command}' not recognized by DirectoryHandler.")
                return None
