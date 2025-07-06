from commands.base import CommandBase
from utils.parser import ParsedCommand


class PHP(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("php")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("PHP not implemented yet!")