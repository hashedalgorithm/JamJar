from models.file_system import FileSystem
from commands.base import CommandBase
from utils.parser import CommandParser, ParsedCommand


class RMDIR(CommandBase):
    def __init__(self, file_system: FileSystem, parsed: ParsedCommand) -> None:
        super().__init__("rmdir")
        self.file_system = file_system
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("RMDIR not implemented yet!")