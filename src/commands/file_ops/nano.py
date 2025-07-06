from commands.base import CommandBase
from utils.parser import ParsedCommand


class NANO(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("nano")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("NANO not implemented yet!")