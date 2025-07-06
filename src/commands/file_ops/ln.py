from commands.base import CommandBase
from utils.parser import ParsedCommand


class LN(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("ln")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("LN not implemented yet!")