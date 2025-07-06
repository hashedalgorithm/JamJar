from commands.base import CommandBase


class PHP(CommandBase):
    def __init__(self) -> None:
        super().__init__("php")

    def run(self) -> str | None:
        raise Exception("PHP not implemented yet!")