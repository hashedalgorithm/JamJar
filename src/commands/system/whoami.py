from commands.base import CommandBase


class WHOAMI(CommandBase):
    def __init__(self) -> None:
        super().__init__("whoami")

    def run(self) -> str | None:
        raise Exception("WHOAMI not implemented yet!")