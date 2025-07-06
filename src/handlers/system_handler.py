from utils.logger import Logger
from utils.parser import CommandParser

from commands.system.df import DF
from commands.system.history import HISTORY
from commands.system.id import ID
from commands.system.last import LAST
from commands.system.php import PHP
from commands.system.uname import UNAME
from commands.system.uptime import UPTIME
from commands.system.w import W
from commands.system.whoami import WHOAMI


class SystemHandler(Logger):
    def __init__(self) -> None:
        super().__init__()
        self.parser = CommandParser()
        self.command_options_map = {
            "df": ["-T", "--type", "--output"],
            "history": [],
            "id": [],
            "last": ["-n", "--limit"],
            "php": ["-f", "-r", "--define", "--php-ini", "--syntax-check", "--file", "--run"],
            "uname": [],
            "uptime": [],
            "w": [],
            "whoami": []
        }

    def handle(self, command: str, full_command: str):
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)
        match command:
            case "df":
                df = DF(parsed)
                return df.run()

            case "history":
                history = HISTORY(parsed)
                return history.run()

            case "php":
                php = PHP(parsed)
                return php.run()

            case "uname":
                uname = UNAME(parsed)
                return uname.run()

            case "whoami":
                whoami = WHOAMI(parsed)
                return whoami.run()

            case "w":
                w = W(parsed)
                return w.run()

            case "id":
                id = ID(parsed)
                return id.run()

            case "last":
                last = LAST(parsed)
                return last.run()

            case "uptime":
                uptime = UPTIME(parsed)
                return uptime.run()

            case _:
                print(f"Command '{command}' not recognized by SystemHandler.")
                return None