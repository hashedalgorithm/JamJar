class CommandBase:
    """
    Base class for all commands.
    """

    def __init__(self, name: str):
        self.name = name

    def run(self, *args, **kwargs):
        """
        Execute the command with the given arguments.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def extract_flags(self, args: list[str]) -> list[str]:
        """
        Extract flags from the command arguments.
        """
        return [arg for arg in args if arg.startswith("-")]

    def extract_paths(self, args: list[str]) -> list[str]:
        """
        Extract paths from the command arguments.
        """
        return [arg for arg in args if not arg.startswith("-")]
