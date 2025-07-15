from typing import Literal
from models.file_system import FileSystem
from models.directory import Directory

TerminalType = Literal[
    "pts"  # Pesudo terminals,
    "tty"  # Virtual terminals
]


class Terminal:
    def __init__(
        self,
        id: int,
        cwd: str,
        uid: int,
        type: TerminalType = "pts",
    ):
        self.id: int = id
        self.uid: int = uid
        self.cwd: str = cwd
        self.type: TerminalType = type
        self.name: str = f"{type}/{id}"


class Terminals:
    def __init__(self, terminals: dict[int, Terminal] = {}):
        self.terminals = terminals

    def get(self, id: int) -> Terminal | None:
        return self.terminals.get(id)

    def add(self, terminal: Terminal) -> Terminal:
        is_exists = self.get(terminal.id)

        if is_exists:
            raise ValueError(f"Terminal already running!")

        self.terminals[terminal.id] = terminal

    def delete(self, id: int) -> None:

        is_exists = self.get(id)

        if not is_exists:
            raise ValueError(f"Terminal not present to delete..")

        del self.terminals[id]

    def is_exists(self, id: int) -> bool:
        terminal = self.get(id)

        return bool(terminal)

    def list_terminals(self) -> list[int]:
        return [terminal.id for terminal in self.terminals.values()]

    def __repr__(self):
        return f"Terminal(name:{self})"
