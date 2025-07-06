from commands.base import CommandBase
from utils.parser import ParsedCommand


class UNZIP(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("unzip")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("UNZIP not implemented yet!")