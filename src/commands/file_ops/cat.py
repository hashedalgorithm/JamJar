from commands.base import CommandBase


class CAT(CommandBase):
    def __init__(self) -> None:
        super().__init__()
        
    def run(self) -> str | None:
        raise Exception("CAT not implemented yet!")