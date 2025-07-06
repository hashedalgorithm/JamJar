from commands.base import CommandBase


class LAST(CommandBase):
    def __init__(self) -> None:
        super().__init__("last")

    def run(self) -> str | None:
        raise Exception("LAST not implemented yet!")