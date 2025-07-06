from commands.base import CommandBase


class IFCONFIG(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def run(self) -> str | None:
        raise Exception("IFCONFIG not implemented yet!")