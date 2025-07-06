from commands.base import CommandBase


class UNAME(CommandBase):
    def __init__(self) -> None:
        super().__init__("uname")

    def run(self) -> str | None:
        raise Exception("UNAME not implemented yet!")