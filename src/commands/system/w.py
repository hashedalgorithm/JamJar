from commands.base import CommandBase
from utils.parser import ParsedCommand


class W(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("w")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("W not implemented yet!")