from handlers.directory_handler import DirectoryHandler
from handlers.network_handler import NetworkHandler
from handlers.process_handler import ProcessHandler
from handlers.file_ops_handler import FileOpsHandler
from handlers.system_handler import SystemHandler
from models.file_system import FileSystem
from models.process_group import ProcessGroup
from models.network_system import NetworkSystem
from utils.logger import Logger


class CommandHandler(Logger):

    def __init__(self) -> None:
        super().__init__()
        self.file_system = FileSystem()
        self.process_group = ProcessGroup()
        self.network_system = NetworkSystem()
        self.directory_handler = DirectoryHandler(file_system=self.file_system)
        self.network_handler = NetworkHandler(network_system=self.network_system)
        self.process_handler = ProcessHandler(process_group=self.process_group)
        self.file_ops_handler = FileOpsHandler()
        self.system_handler = SystemHandler()

    def invoke_directory_handler(self, command: str, full_command: str):
        self.logger.info(f"Captured - {command}")
        return self.directory_handler.handle(command, full_command)

    def invoke_network_handler(self, command: str, full_command: str):
        self.logger.info(f"Captured - {command}")
        return self.network_handler.handle(command, full_command)

    def invoke_process_handler(
        self, command: str, full_command: str, tty: int, pid: int
    ):
        self.logger.info(f"Captured - {command}")
        return self.process_handler.handle(command, full_command, tty=tty, pid=pid)

    def invoke_file_ops_handler(self, command: str, full_command: str):
        self.logger.info(f"Captured - {command}")
        return self.file_ops_handler.handle(command, full_command)

    def invoke_system_handler(self, command: str, full_command: str):
        self.logger.info(f"Captured - {command}")
        return self.system_handler.handle(command, full_command)
