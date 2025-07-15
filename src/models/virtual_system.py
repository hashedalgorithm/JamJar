from models.terminals import Terminals, Terminal
from models.file_system import FileSystem
from models.process_group import ProcessGroup
from models.network_system import NetworkSystem
from models.user_manager import UserManager


class VirtualSystem:
    def __init__(self):
        self.user_manager: UserManager = UserManager()
        self.file_system: FileSystem = FileSystem()
        self.terminals: Terminals = Terminals()
        self.process_group = ProcessGroup()
        self.network_system = NetworkSystem()

    def get_terminal(self, id: int) -> Terminal:
        return self.terminals.get(id)

    def __repr__(self):
        return f"Virtual System ( users: {len(self.user_manager.users)}; terminals: {len(self.terminals)} )"
