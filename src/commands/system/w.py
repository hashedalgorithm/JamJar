from commands.base import CommandBase


class W(CommandBase):
    def __init__(self) -> None:
        super().__init__("w")

    def run(self) -> str | None:
        raise Exception("W not implemented yet!")