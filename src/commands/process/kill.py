from commands.base import CommandBase
from models.process import Process
from utils import helper


class KILL(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def kill(self, args):
        valid_arg = False

        target_process, _ = helper.get_main_arg_helper(args)

        for process in self.processes:
            if process.pid == target_process:
                self.processes.remove(process)
                valid_arg = True

        if not valid_arg:
            return f"bash: kill: {target_process}: arguments must be process or job IDs"
        
    def run(self) -> str | None:
        raise Exception("KILL not implemented yet!")