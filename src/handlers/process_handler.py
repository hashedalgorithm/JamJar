from utils import helper
from utils.logger import Logger
from utils.parser import CommandParser

from commands.process.kill import KILL
from commands.process.killall import KILLALL
from commands.process.ps import PS


class ProcessHandler(Logger):
    def __init__(self) -> None:
        super().__init__()
        self.processes = helper.create_fake_processes()
        self.parser = CommandParser()
        self.command_options_map = {
            "kill": ["-s", "--signal", "-n"],
            "killall": [
                "-s",
                "--signal",
                "-u",
                "--user",
                "-n",
                "--ns",
                "-Z",
                "--context",
            ],
            "ps": [
                "-C",
                "-G",
                "-g",
                "-p",
                "-q",
                "-t",
                "-U",
                "-u",
                "-o",
                "--sort",
                "--ppid",
                "--pid",
                "--tty",
                "--user",
            ],
        }

    def handle(self, command: str, full_command: str, tty: str, pid: int):
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)

        match command:
            case "ps":
                ps = PS(self.processes, parsed)
                return ps.run(tty, pid)

            case "kill":
                kill = KILL(self.processes)
                return kill.run(parsed, tty, pid)

            case "killall":
                killall = KILLALL(self.processes)
                return killall.run(parsed)

            case _:
                self.logger.info(
                    f"Command '{command}' not recognized by ProcessHandler."
                )
                return None
