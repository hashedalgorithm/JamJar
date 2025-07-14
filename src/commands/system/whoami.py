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

    def get_help(self) -> list[str]:
        return f"""
Usage: whoami [OPTION]...
Print the user name associated with the current effective user ID.
Same as id -un.

      --help        display this help and exit
      --version     output version information and exit

GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
Full documentation <https://www.gnu.org/software/coreutils/whoami>
or available locally via: info '(coreutils) whoami invocation'
hashedalgorithm@VM:~$ 

        """

    def get_version(self) -> list[str]:
        return f"""
whoami (GNU coreutils) {self.version}
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Richard Mlynarik.

        """
