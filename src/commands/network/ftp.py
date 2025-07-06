from commands.base import CommandBase
from utils.parser import ParsedCommand


class FTP(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("ftp")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("FTP not implemented yet!")