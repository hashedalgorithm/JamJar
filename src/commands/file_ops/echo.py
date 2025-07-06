from commands.base import CommandBase


class ECHO(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def run(self) -> str | None:
        raise Exception("ECHO not implemented yet!")