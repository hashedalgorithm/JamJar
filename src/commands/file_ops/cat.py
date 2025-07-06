from commands.base import CommandBase
### gets stuck while running command even though there is nothing in the code
from utils.parser import ParsedCommand

class CAT(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("cat")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("CAT not implemented yet!")
    