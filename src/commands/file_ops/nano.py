from commands.base import CommandBase


class NANO(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def run(self) -> str | None:
        raise Exception("NANO not implemented yet!")