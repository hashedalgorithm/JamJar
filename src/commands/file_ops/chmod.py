from commands.base import CommandBase


class CHMOD(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def run(self) -> str | None:
        raise Exception("CHMOD not implemented yet!")