from commands.base import CommandBase
from utils.parser import ParsedCommand
from models.users import User


class WHOAMI(CommandBase):

    other_flags: set[str] = {
        # Others
        "--help",  # display this help and exit
        "--version",  # output version information and exit
    }

    def __init__(self, user: User, parsed: ParsedCommand) -> None:
        super().__init__("whoami", "9.4")
        self.parsed = parsed
        self.user: User = user

    def default(self) -> str:
        return self.user.username

    def run(self) -> str | None:
        if self.parsed.args.__len__() == 0:
            return self.default()

        if self.parsed.find("--help"):
            return self.get_help()

        if self.parsed.find("--version"):
            return self.get_version()

        return self.default()
