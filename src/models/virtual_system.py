from models.users import User, Users
from models.terminals import Terminals, Terminal
from models.file_system import FileSystem
from models.process_group import ProcessGroup
from models.network_system import NetworkSystem


class VirtualSystem:
    def __init__(self):
        self.users: Users = Users()
        self.file_system: FileSystem = FileSystem()
        self.terminals: Terminals = Terminals(file_system=self.file_system)
        self.process_group = ProcessGroup()
        self.network_system = NetworkSystem()

    def get_terminal(self, id: int) -> Terminal:
        return self.terminals.get(id)

    def get_user(self, uid: int) -> User:
        return self.users.get(uid)

    def __repr__(self):
        return f"Virtual System ( users: {len(self.users)}; terminals: {len(self.terminals)} )"
