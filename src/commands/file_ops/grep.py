from commands.base import CommandBase
from utils.parser import ParsedCommand


class GREP(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("grep")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("GREP not implemented yet!")