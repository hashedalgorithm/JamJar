from commands.base import CommandBase
from utils.parser import ParsedCommand


class HISTORY(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("history")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("HISTORY not implemented yet!")