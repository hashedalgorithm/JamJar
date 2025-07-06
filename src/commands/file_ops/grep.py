from commands.base import CommandBase


class GREP(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def run(self) -> str | None:
        raise Exception("GREP not implemented yet!")