from commands.base import CommandBase
from utils.parser import ParsedCommand


class CHMOD(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("chmod")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("CHMOD not implemented yet!")