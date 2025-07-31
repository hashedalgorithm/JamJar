from typing import Literal
import struct, termios, fcntl
from utils.logger import Logger

TerminalType = Literal[
    "pts"  # Pesudo terminals,
    "tty"  # Virtual terminals
]


class Terminal(Logger):
    def __init__(
        self,
        cwd: str,
        uid: int,
        id: int | None = None,
        tty: str | None = None,
    ):
        super().__init__()
        if id and tty:
            raise ValueError("Either only id or tty should be present!")

        _id = id if id else self.extract_id_from_tty(tty)
        self.id: int = _id
        self.uid: int = uid
        self.cwd: str = cwd
        self.type: TerminalType = tty if self.extract_type_from_tty(tty) else "pts"
        self.tty: str = tty if tty else f"{type}/{_id}"
        self.terminal_path: str = f"/dev/{self.tty}"
        self.size: tuple[int, int] = self.get_tty_width(
            self.terminal_path
        )  # [row, columns]

    def with_cwd(self, path: str) -> str:
        """path: is relative path for eg. sample/somefolder"""

        return f"{self.cwd}/{path}"

    def extract_id_from_tty(self, tty: str) -> int:
        id = tty.split("/")[-1]

        if id:
            return int(id)
        else:
            return 1

    def extract_type_from_tty(self, tty: str) -> TerminalType:
        type = tty.split("/")[0]

        if type != "pts" and type != "tty":
            raise ValueError(f"Invalid tty found! - {tty}")

        return type

    def set_cwd(self, path: str) -> None:
        self.cwd = path

    def get_tty_width(self, terminal_path: str) -> tuple[int, int]:
        try:
            with open(terminal_path) as tty:
                rows, cols = struct.unpack(
                    "hh", fcntl.ioctl(tty, termios.TIOCGWINSZ, "1234")
                )
                return rows, cols
        except Exception as e:
            self.logger.warning(f"Couldn't find terminal -{terminal_path} size:  {e}")
            return 24, 80


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

    def extract_id_from_tty(self, tty: str) -> int:
        return int(tty.split("/")[-1])

    def __repr__(self):
        return f"Terminal(name:{self})"
