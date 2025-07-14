class CommandBase:
    """
    Base class for all commands.
    """

    def __init__(self, name: str, version: str = "v0"):
        self.name = name
        self.version: str = version

    def run(self, *args, **kwargs):
        """
        Execute the command with the given arguments.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def default(self):
        """
        Return default behaviour of the command without any args
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_help(self) -> list[str]:
        """
        Return help readme
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_version(self) -> list[str]:
        """Return version readme"""
        raise NotImplementedError("Subclasses must implement this method")

    def print(self, output: list[str]) -> str:
        """Returns single string"""
        return "\n".join(output)
