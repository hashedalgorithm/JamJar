from commands.base import CommandBase
from models.process import Process
from utils.parser import ParsedCommand
from utils import helper


class KILLALL(CommandBase):
    def __init__(self, processes: Process, parsed: ParsedCommand) -> None:
        super().__init__("killall")
        self.processes = processes
        self.parsed = parsed

    def killall(self, args):

        valid_arg = False

        target_process, _ = helper.get_main_arg_helper(args)

        for process in self.processes:
            if process.command == target_process:
                self.processes.remove(process)
                valid_arg = True

        if not valid_arg:
            return f"{target_process}: no process found"
        
    def run(self) -> str | None:
        raise Exception("KILLALL not implemented yet!")