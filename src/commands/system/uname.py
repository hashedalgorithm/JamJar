from commands.base import CommandBase


class UNAME(CommandBase):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> str | None:
        raise Exception("UNAME not implemented yet!")