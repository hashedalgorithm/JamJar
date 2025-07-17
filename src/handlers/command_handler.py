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

    def sync_virtual_system(self, tty: str, cwd: str, uid: int, gid: int) -> Terminal:
        terminal_id = self.virtual_system.terminals.extract_id_from_tty(tty=tty)

        terminal = self.virtual_system.terminals.get(id=terminal_id)

        is_user_exists, is_group_exists = (
            self.virtual_system.user_manager.is_user_and_group_exists(
                uid=terminal.uid, gid=gid
            )
        )

        if not terminal:
            self.logger.info(f"New terminal captured, running on uid: {uid}!")
            self.virtual_system.terminals.add(
                Terminal(
                    tty=tty,
                    cwd=cwd,
                    uid=uid,
                )
            )
        else:
            if terminal.cwd != cwd:
                self.logger.info(f"cwd of {terminal.tty} is changed to {cwd}")
                self.virtual_system.terminals.set_cwd(id=terminal.id, path=cwd)

        if not is_user_exists:
            self.logger.info(f"New user captured! - {uid} is active")
            self.virtual_system.user_manager.add_user(
                User(uid=uid, terminals=[terminal_id])
            )

        if not is_group_exists:
            self.logger.info(f"New Group captured! - {gid} is created")
            user = self.virtual_system.user_manager.get_user(uid)
            self.virtual_system.user_manager.add_group(
                Group(gid=gid, group_username=user.username)
            )

        return terminal

    def log_command_details(self, command: str, uid: int, tty: str, cwd: str) -> None:
        self.logger.info(f"{uid} : Captured - {command} at {tty}:{cwd}")

    def invoke_directory_handler(
        self, command: str, full_command: str, uid: int, gid: int, tty: str, cwd: str
    ):
        terminal = self.sync_virtual_system(tty=tty, cwd=cwd, uid=uid, gid=gid)
        self.log_command_details(
            command=command, uid=terminal.uid, tty=terminal.tty, cwd=terminal.cwd
        )

        return self.directory_handler.handle(
            command=command, full_command=full_command, terminal=terminal
        )

    def invoke_network_handler(
        self, command: str, full_command: str, uid: int, gid: int, tty: str, cwd: str
    ):
        terminal = self.sync_virtual_system(tty=tty, cwd=cwd, uid=uid, gid=gid)
        self.log_command_details(command=command, uid=uid, tty=tty, cwd=cwd)

        return self.network_handler.handle(
            command=command, full_command=full_command, terminal=terminal
        )

    def invoke_process_handler(
        self,
        command: str,
        full_command: str,
        uid: int,
        gid: int,
        pid: int,
        tty: int,
        cwd: str,
    ):
        terminal = self.sync_virtual_system(tty=tty, cwd=cwd, uid=uid, gid=gid)
        self.log_command_details(command=command, uid=uid, tty=tty, cwd=cwd)

        return self.process_handler.handle(
            command=command,
            full_command=full_command,
            terminal=terminal,
            pid=pid,
        )

    def invoke_file_ops_handler(
        self, command: str, full_command: str, uid: int, gid: int, tty: str, cwd: str
    ):
        terminal = self.sync_virtual_system(tty=tty, cwd=cwd, uid=uid, gid=gid)
        self.log_command_details(command=command, uid=uid, tty=tty, cwd=cwd)

        return self.file_ops_handler.handle(
            command=command, full_command=full_command, terminal=terminal
        )

    def invoke_system_handler(
        self,
        command: str,
        full_command: str,
        uid: int,
        gid: int,
        tty: str,
        cwd: str,
    ):
        terminal = self.sync_virtual_system(tty=tty, cwd=cwd, uid=uid, gid=gid)
        self.log_command_details(command=command, uid=uid, tty=tty, cwd=cwd)

        return self.system_handler.handle(
            command=command, full_command=full_command, terminal=terminal, gid=gid
        )
