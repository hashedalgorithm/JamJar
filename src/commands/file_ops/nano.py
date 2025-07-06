from commands.base import CommandBase


class NANO(CommandBase):
    def __init__(self) -> None:
        super().__init__("nano")
        
    def run(self) -> str | None:
        raise Exception("NANO not implemented yet!")