from commands.base import CommandBase
from utils.parser import ParsedCommand


class WHOAMI(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("whoami")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("WHOAMI not implemented yet!")