from commands.base import CommandBase


class ID(CommandBase):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> str | None:
        raise Exception("ID not implemented yet!")