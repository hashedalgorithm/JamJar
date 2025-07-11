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

    def help(self) -> list[str]:
        """
        Return help readme
        """
        raise NotImplementedError("Subclasses must implement this method")

    def version(self) -> list[str]:
        """Return version readme"""
        raise NotImplementedError("Subclasses must implement this method")
