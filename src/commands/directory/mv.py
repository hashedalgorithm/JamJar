from models.file_system import FileSystem
from commands.base import CommandBase


class MV(CommandBase):
    def __init__(self, file_system: FileSystem) -> None:
        super().__init__("mv")
        self.file_system = file_system
        
    def run(self) -> str | None:
        raise Exception("MV not implemented yet!")