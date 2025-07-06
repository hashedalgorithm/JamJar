from commands.base import CommandBase


class HISTORY(CommandBase):
    def __init__(self) -> None:
        super().__init__("history")

    def run(self) -> str | None:
        raise Exception("HISTORY not implemented yet!")