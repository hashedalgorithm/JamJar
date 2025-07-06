from commands.base import CommandBase
from utils.parser import ParsedCommand


class VI(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("vi")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("VI not implemented yet!")