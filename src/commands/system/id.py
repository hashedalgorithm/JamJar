from commands.base import CommandBase
from utils.parser import ParsedCommand
from models.user_manager import UserManager
from models.users import User
from models.groups import Group


class ID(CommandBase):

    format_flags: set[str] = {
        "-a",  # ignore, for compatibility with other versions
        "-Z",  # print only the security context of the process
        "--context",  # print only the security context of the process
        "-g",  # print only the effective group ID
        "--group",  # print only the effective group ID
        "-G",  # print all group IDs
        "--groups",  # print all group IDs
        "-n",  # print a name instead of a number, for -ugG
        "--name",  # print a name instead of a number, for -ugG
        "-r",  # print the real ID instead of the effective ID, with -ugG
        "--real",  # print the real ID instead of the effective ID, with -ugG
        "-u",  # print only the effective user ID
        "--user",  # print only the effective user ID
        "-z",  # delimit entries with NUL characters, not whitespace; not permitted in default format
        "--zero",  # delimit entries with NUL characters, not whitespace; not permitted in default format
    }

    other_flags: set[str] = {
        "--help",  # display this help and exit
        "--version",  # output version information and exit
    }

    def __init__(
        self, parsed: ParsedCommand, uid: int, gid: int, user_manager: UserManager
    ) -> None:
        super().__init__("id", "9.4")
        self.parsed = parsed
        self.user_manager = user_manager
        self.uid = uid
        self.gid = gid

    def print_entry(self) -> str:
        # user = self.user_manager.get_user()

        # uid = f"uid={self.user.uid}({self.user.username}"
        # gid = f"gid={self.user.gid}({self.group.group_username})"
        # groups = f"groups="

        # for group in self.user.groups:
        #     pass

        return f")"

    def default(self):
        # uid=1000(hashedalgorithm) gid=1000(hashedalgorithm)
        # groups=1000(hashedalgorithm),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),100(users),114(lpadmin)

        # output = f"uid:{self.user.uid}({self.user.username})"

        return f"vankam di mappale"

    def run(self) -> str | None:
        output: list[str] = ["vada yen machi"]

        if len(self.parsed.args) == 0:
            return self.print(self.default())

        return self.print(output)

    def get_version(self):
        return f"""
id (GNU coreutils) {self.version}
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Arnold Robbins and David MacKenzie.

        """

    def get_help(self):
        return f"""
Usage: id [OPTION]... [USER]...
Print user and group information for each specified USER,
or (when USER omitted) for the current process.

  -a             ignore, for compatibility with other versions
  -Z, --context  print only the security context of the process
  -g, --group    print only the effective group ID
  -G, --groups   print all group IDs
  -n, --name     print a name instead of a number, for -ugG
  -r, --real     print the real ID instead of the effective ID, with -ugG
  -u, --user     print only the effective user ID
  -z, --zero     delimit entries with NUL characters, not whitespace;
                   not permitted in default format
      --help        display this help and exit
      --version     output version information and exit

Without any OPTION, print some useful set of identified information.

GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
Full documentation <https://www.gnu.org/software/coreutils/id>
or available locally via: info '(coreutils) id invocation'

        """
