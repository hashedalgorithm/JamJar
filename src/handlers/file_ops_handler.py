from utils.logger import Logger
from utils.parser import CommandParser

from commands.file_ops.cat import CAT
from commands.file_ops.chmod import CHMOD
from commands.file_ops.crontab import CRONTAB
from commands.file_ops.echo import ECHO
from commands.file_ops.grep import GREP
from commands.file_ops.ln import LN
from commands.file_ops.nano import NANO
from commands.file_ops.touch import TOUCH
from commands.file_ops.unzip import UNZIP
from commands.file_ops.vi import VI


class FileOpsHandler(Logger):
    def __int__(self):
        super().__init__()
        self.parser = CommandParser()
        self.command_options_map = {
            "cat": [],
            "chmod": ["--reference"],
            "crontab": ["-u"],
            "echo": [],
            "grep": ["-e", "--regexp", "-f", "--file", "-m", "--max-count", "--label", "--binary-files", "-d", "--directories", "-D", "--devices", "--include", "--exclude", "--exclude-from", "--exclude-dir", "-B", "--before-context", "-A", "--after-context", "-C", "--context", "--group-separator", "--color", "--colour"],
            "ln": ["--backup", "-S", "--suffix", "-t", "--target-directory"],
            "nano": ["-C", "--backupdir", "-J", "--guidestripe", "-Q", "--quotestr", "-T", "--tabsize", "-X", "--wordchars", "-Y", "--syntax", "-f", "--rcfile", "-o", "--operatingdir", "-r", "--fill", "-s", "--speller"],
            "touch": ["-d", "--date", "-r", "--reference", "--time"],
            "unzip": ["-O", "-I"],
            "vi": ["-T", "-u", "--cmd", "-c", "-S", "-s", "-w", "-W"]
        }

    def handle(self, command: str, full_command: str):
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)
        match command:
            case "touch":
                touch = TOUCH()
                return touch.run(parsed)

            case "cat":
                cat = CAT()
                return cat.run(parsed)

            case "grep":
                grep = GREP()
                return grep.run(parsed)

            case "echo":
                echo = ECHO()
                return echo.run(parsed)

            case "unzip":
                unzip = UNZIP()
                return unzip.run(parsed)

            case "chmod":
                chmod = CHMOD()
                return chmod.run(parsed)

            case "nano":
                nano = NANO()
                return nano.run(parsed)

            case "vi":
                vi = VI()
                return vi.run(parsed)

            case "ln":
                ln = LN()
                return ln.run(parsed)

            case "crontab":
                crontab = CRONTAB()
                return crontab.run(parsed)

            case _:
                print(f"Command '{command}' not recognized by FileOpsHandler.")
                return None
