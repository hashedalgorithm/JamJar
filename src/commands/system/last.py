from commands.base import CommandBase
from utils.parser import ParsedCommand


class LAST(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("last")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("LAST not implemented yet!")