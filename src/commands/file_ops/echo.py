from commands.base import CommandBase
from utils.parser import ParsedCommand


class ECHO(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("echo")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("ECHO not implemented yet!")