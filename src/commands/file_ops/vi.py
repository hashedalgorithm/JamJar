from commands.base import CommandBase


class VI(CommandBase):
    def __init__(self) -> None:
        super().__init__("vi")

    def run(self) -> str | None:
        raise Exception("VI not implemented yet!")