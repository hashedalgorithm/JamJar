from commands.base import CommandBase


class NMAP(CommandBase):
    def __init__(self) -> None:
        super().__init__("nmap")
        
    def run(self) -> str | None:
        raise Exception("NMAP not implemented yet!")