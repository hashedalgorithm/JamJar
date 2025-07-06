from commands.base import CommandBase
from utils.parser import ParsedCommand


class DF(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("df")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("DF not implemented yet!")