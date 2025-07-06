from commands.base import CommandBase
from utils.parser import ParsedCommand


class IFCONFIG(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("ifconfig")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("IFCONFIG not implemented yet!")