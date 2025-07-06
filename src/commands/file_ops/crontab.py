from commands.base import CommandBase


class CRONTAB(CommandBase):
    def __init__(self) -> None:
        super().__init__("crontab")
        
    def run(self) -> str | None:
        raise Exception("CRONTAB not implemented yet!")