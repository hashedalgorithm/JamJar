from utils.logger import Logger
from utils.parser import CommandParser
from models.process_group import ProcessGroup

from commands.process.kill import KILL
from commands.process.killall import KILLALL
from commands.process.ps import PS


class ProcessHandler(Logger):
    def __init__(self, process_group: ProcessGroup) -> None:
        super().__init__()
        self.process_group = process_group
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
                ps = PS(self.process_group.processes, parsed)
                return ps.run(tty, pid)

            case "kill":
                kill = KILL(self.process_group.processes, parsed)
                return kill.run(tty, pid)

            case "killall":
                killall = KILLALL(self.process_group.processes, parsed)
                return killall.run()

            case _:
                self.logger.info(
                    f"Command '{command}' not recognized by ProcessHandler."
                )
                return None
