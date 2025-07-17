from commands.base import CommandBase
from utils import helper
from models.file import File
from utils.parser import ParsedCommand
from models.file_system import FileSystem


class TOUCH(CommandBase):

    operational_flags: set[str] = {
        "-a",  # change only the access time
        "-c",  # do not create any files
        "--no-create",  # do not create any files
        "-d",  # parse STRING and use it instead of current time
        "--date",  # parse STRING and use it instead of current time
        "-f",  # (ignored)
        "-h",  # affect each symbolic link instead of any referenced file
        "--no-dereference",  # affect each symbolic link instead of any referenced file
        "-m",  # change only the modification time
        "-r",  # use this file's times instead of current time
        "--reference",  # use this file's times instead of current time
        "-t",  # use [[CC]YY]MMDDhhmm[.ss] instead of current time
        "--time",  # change the specified time (access/modify)
    }

    other_flags: set[str] = {
        # Others
        "--help",  # display this help and exit
        "--version",  # output version information and exit
    }

    def __init__(
        self, parsed: ParsedCommand, file_system: FileSystem, cwd: str
    ) -> None:
        super().__init__("touch")
        self.parsed = parsed
        self.file_system = file_system
        self.cwd = cwd


    def run(self) -> str | None:

        output: list[str] = []

        if len(self.parsed.args) == 0:
            return self.default()

        if self.parsed.find("--help"):
            return self.get_help()

        if self.parsed.find("--version"):
            return self.get_version()

        return self.print(output)

