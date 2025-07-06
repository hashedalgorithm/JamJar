from commands.base import CommandBase


class DF(CommandBase):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> str | None:
        raise Exception("DF not implemented yet!")