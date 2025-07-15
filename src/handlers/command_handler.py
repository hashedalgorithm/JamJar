from handlers.directory_handler import DirectoryHandler
from handlers.network_handler import NetworkHandler
from handlers.process_handler import ProcessHandler
from handlers.file_ops_handler import FileOpsHandler
from handlers.system_handler import SystemHandler
from models.virtual_system import VirtualSystem
from models.terminals import Terminal
from models.groups import Group
from models.users import User
from utils.logger import Logger


class CommandHandler(Logger):

    def __init__(self) -> None:
        super().__init__()
        self.virtual_system = VirtualSystem()
        self.directory_handler = DirectoryHandler(
            file_system=self.virtual_system.file_system
        )
        self.network_handler = NetworkHandler(
            network_system=self.virtual_system.network_system
        )
        self.process_handler = ProcessHandler(
            process_group=self.virtual_system.process_group
        )
        self.file_ops_handler = FileOpsHandler(
            file_system=self.virtual_system.file_system
        )
        self.system_handler = SystemHandler(
            user_manager=self.virtual_system.user_manager
        )

    def sync_virtual_system(self, id: int, uid: int, gid: int) -> None:
        is_terminal_exists = self.virtual_system.terminals.is_exists(id)
        is_user_exists, is_group_exists = (
            self.virtual_system.user_manager.is_user_and_group_exists(uid, gid)
        )

        if not is_terminal_exists:
            self.logger.info(f"New terminal captured, running on uid: {uid}!")
            self.virtual_system.terminals.add(
                Terminal(
                    id=id,
                    cwd=self.virtual_system.file_system.get_default_cwd(uid).get_path(),
                    uid=uid,
                )
            )

        if not is_user_exists:
            self.logger.info(f"New user captured! - {uid} is active")
            self.virtual_system.user_manager.add_user(User(uid=uid, terminals=[id]))

        if not is_group_exists:
            self.logger.info(f"New Group captured! - {gid} is created")
            user = self.virtual_system.user_manager.get_user(uid)
            self.virtual_system.user_manager.add_group(
                Group(gid=gid, group_username=user.username)
            )

    def invoke_directory_handler(
        self, command: str, full_command: str, uid: int, tty: str, cwd: str
    ):
        self.logger.info(f"{uid} : Captured - {command} at {tty}:{cwd}")
        return self.directory_handler.handle(command, full_command, cwd)

    def invoke_network_handler(self, command: str, full_command: str):
        self.logger.info(f"Captured - {command}")
        return self.network_handler.handle(command, full_command)

    def invoke_process_handler(
        self, command: str, full_command: str, tty: int, pid: int
    ):
        self.logger.info(f"Captured - {command}")
        return self.process_handler.handle(command, full_command, tty=tty, pid=pid)

    def invoke_file_ops_handler(self, command: str, full_command: str, cwd: str):
        self.logger.info(f"Captured - {command}")
        return self.file_ops_handler.handle(command, full_command, cwd)

    def invoke_system_handler(
        self, command: str, full_command: str, uid: int, gid: int
    ):
        self.logger.info(f"{uid} : Captured - {command} ")
        return self.system_handler.handle(command, full_command, uid, gid)
