from commands.base import CommandBase
from utils.parser import ParsedCommand
from models.network_system import NetworkInterface


class IFCONFIG(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("ifconfig")
        self.parsed = parsed

    def run(self, interfaces: dict[str, NetworkInterface]) -> str | None:
        raise Exception("IFCONFIG not implemented yet!")
