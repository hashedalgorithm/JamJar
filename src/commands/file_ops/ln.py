from commands.base import CommandBase


class LN(CommandBase):
    def __init__(self) -> None:
        super().__init__("ln")
        
    def run(self) -> str | None:
        raise Exception("LN not implemented yet!")