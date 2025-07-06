from commands.base import CommandBase
from utils.parser import ParsedCommand


class UPTIME(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("uptime")
        self.parsed = parsed

    def run(self) -> str | None:
        raise Exception("UPTIME not implemented yet!")