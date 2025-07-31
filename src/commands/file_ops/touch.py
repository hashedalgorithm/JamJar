from commands.base import CommandBase
from utils import helper
from models.file import File
from utils.parser import ParsedCommand, ParsedArgument
from models.file_system import FileSystem, ParsedPath
from models.terminals import Terminal
import datetime


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
        self, parsed: ParsedCommand, file_system: FileSystem, terminal: Terminal
    ) -> None:
        super().__init__("touch")
        self.parsed = parsed
        self.file_system = file_system
        self.terminal = terminal

    def create_file(self, path: str, filename: str) -> str:
        try:
            entity = self.file_system.get_directory(path)

            entity.add(File(name=filename, content="", size=0))
            return f""
        except ValueError:
            return f"touch: cannot touch '{path}/{filename}': No such file or directory"

    def process_path(self, path: str) -> tuple[str, str]:
        filename = path
        _path = self.terminal.cwd

        if path.startswith("/"):
            segments = path.split("/")

            filename = segments.pop()
            _path = f"/{"/".join(segments)}"

        if path.find("/") != -1:
            segments = path.split("/")

            filename = segments.pop()
            _path = self.terminal.with_cwd("/".join(segments))

        return _path, filename

    def run(self) -> str | None:

        output: list[str] = []

        if len(self.parsed.args) == 0:
            return self.default()

        if self.parsed.find("--help"):
            return self.get_help()

        if self.parsed.find("--version"):
            return self.get_version()

        positional_args = self.parsed.group(["positional"], {})
        source_paths = (
            [ParsedArgument(type="positional", value=self.terminal.cwd)]
            if len(positional_args) == 0
            else positional_args
        )

        for source_path in source_paths:
            if not source_path.value:
                continue

            _path, filename = self.process_path(source_path.value)

            _out = self.create_file(path=_path, filename=filename)
            if _out:
                output.append(_out)

        return self.print(output)
