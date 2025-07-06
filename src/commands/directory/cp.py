from models.file_system import FileSystem
from commands.base import CommandBase


class CP(CommandBase):
    def __init__(self, file_system: FileSystem) -> None:
        super().__init__()
        self.file_system = file_system
        
    def run(self) -> str | None:
        raise Exception("CP not implemented yet!")