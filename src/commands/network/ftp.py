from commands.base import CommandBase


class FTP(CommandBase):
    def __init__(self) -> None:
        super().__init__("ftp")
        
    def run(self) -> str | None:
        raise Exception("FTP not implemented yet!")