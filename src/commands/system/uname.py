from commands.base import CommandBase
from utils.parser import ParsedCommand


class UNAME(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("uname")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("UNAME not implemented yet!")