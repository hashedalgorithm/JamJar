class Flagmap:

    def __init__(self):
        pass

    def set_flag(self, flag: str, value: bool) -> None:
        if hasattr(self, flag):
            setattr(self, flag, value)


class FlagWithArgument:
    def __init__(self, flag: str, argument: str | None = None) -> None:
        self.flag = flag
        self.argument = argument

    def set_argument(self, argument: str) -> None:
        self.argument = argument

    def get_flag(self) -> str:
        return self.flag

    def get_argument(self) -> str:
        return self.argument

    def get(self) -> str:
        return f"{self.flag} {self.argument}" if self.argument else self.flag
