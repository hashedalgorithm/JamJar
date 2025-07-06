from commands.base import CommandBase


class LAST(CommandBase):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> str | None:
        raise Exception("LAST not implemented yet!")