from commands.base import CommandBase
from utils.parser import ParsedCommand


class CRONTAB(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("crontab")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("CRONTAB not implemented yet!")