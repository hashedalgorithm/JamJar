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
    def __init__(self) -> None:
        super().__init__()
        self.parser = CommandParser()
        self.command_options_map = {
            "cat": [],
            "chmod": ["--reference"],
            "crontab": ["-u"],
            "echo": [],
            "grep": [
                "-e",
                "--regexp",
                "-f",
                "--file",
                "-m",
                "--max-count",
                "--label",
                "--binary-files",
                "-d",
                "--directories",
                "-D",
                "--devices",
                "--include",
                "--exclude",
                "--exclude-from",
                "--exclude-dir",
                "-B",
                "--before-context",
                "-A",
                "--after-context",
                "-C",
                "--context",
                "--group-separator",
                "--color",
                "--colour",
            ],
            "ln": ["--backup", "-S", "--suffix", "-t", "--target-directory"],
            "nano": [
                "-C",
                "--backupdir",
                "-J",
                "--guidestripe",
                "-Q",
                "--quotestr",
                "-T",
                "--tabsize",
                "-X",
                "--wordchars",
                "-Y",
                "--syntax",
                "-f",
                "--rcfile",
                "-o",
                "--operatingdir",
                "-r",
                "--fill",
                "-s",
                "--speller",
            ],
            "touch": ["-d", "--date", "-r", "--reference", "--time"],
            "unzip": ["-O", "-I"],
            "vi": ["-T", "-u", "--cmd", "-c", "-S", "-s", "-w", "-W"],
        }

    def handle(self, command: str, full_command: str) -> str | None:
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)
        match command:
            case "touch":
                touch = TOUCH(parsed)
                return touch.run()

            case "cat":
                cat = CAT(parsed)
                return cat.run()

            case "grep":
                grep = GREP(parsed)
                return grep.run()

            case "echo":
                echo = ECHO(parsed)
                return echo.run()

            case "unzip":
                unzip = UNZIP(parsed)
                return unzip.run()

            case "chmod":
                chmod = CHMOD(parsed)
                return chmod.run()

            case "nano":
                nano = NANO(parsed)
                return nano.run()

            case "vi":
                vi = VI(parsed)
                return vi.run()

            case "ln":
                ln = LN(parsed)
                return ln.run()

            case "crontab":
                crontab = CRONTAB(parsed)
                return crontab.run()

            case _:
                self.logger.error(
                    f"Command '{command}' not recognized by FileOpsHandler."
                )
                return None
