from commands.base import CommandBase
from utils.parser import ParsedCommand


class ID(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("id")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("ID not implemented yet!")