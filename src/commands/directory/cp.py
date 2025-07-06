from models.file_system import FileSystem
from commands.base import CommandBase
from utils.parser import CommandParser, ParsedCommand


class CP(CommandBase):
    def __init__(self, file_system: FileSystem, parsed: ParsedCommand) -> None:
        super().__init__("cp")
        self.file_system = file_system
        self.parsed = parsed
        
    def run(self) -> str | None:
        if not self.parsed.args:
            return "cp: missing operand\nTry 'rm --help' for more information."