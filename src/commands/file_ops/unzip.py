from commands.base import CommandBase


class UNZIP(CommandBase):
    def __init__(self) -> None:
        super().__init__("unzip")
        
    def run(self) -> str | None:
        raise Exception("UNZIP not implemented yet!")