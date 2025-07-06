from commands.base import CommandBase
from utils.parser import ParsedCommand


class NMAP(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("nmap")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("NMAP not implemented yet!")