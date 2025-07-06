from commands.base import CommandBase


class UPTIME(CommandBase):
    def __init__(self) -> None:
        super().__init__("uptime")

    def run(self) -> str | None:
        raise Exception("UPTIME not implemented yet!")