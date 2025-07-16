from typing import Literal

TerminalType = Literal[
    "pts"  # Pesudo terminals,
    "tty"  # Virtual terminals
]


class Terminal:
    def __init__(
        self,
        cwd: str,
        uid: int,
        id: int | None = None,
        type: TerminalType = "pts",
        tty: str | None = None,
    ):
        if id and tty:
            raise ValueError("Either only id or tty should be present!")

        _id = id if id else self.extract_id_from_tty(tty)
        self.id: int = _id
        self.uid: int = uid
        self.cwd: str = cwd
        self.type: TerminalType = type
        self.tty: str = tty if tty else f"{type}/{_id}"

    def extract_id_from_tty(self, tty: str) -> int:
        return int(tty.split("/")[-1])

    def set_cwd(self, path: str) -> None:
        self.cwd = path


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

    def set_cwd(self, id: int, path: str) -> None:
        terminal = self.terminals.get(id)

        if not terminal:
            raise ValueError(f"Terminal not found!")

        terminal.set_cwd(path)

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
