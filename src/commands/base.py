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

    def initialize_flag_map(self, flags: list[str]) -> dict:
        """
        Initialize the flag map based on the provided flags.
        """
        raise NotImplementedError("Subclasses must implement this method.")
