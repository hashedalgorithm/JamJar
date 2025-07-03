from models.file_system import FileSystem


class LS:
    def __init__(self, file_system: FileSystem, args: list[str] = []) -> None:
        self.file_system = file_system
        self.paths = self.extract_paths(args)
        self.extract_options = self.extract_options(args)

    def extract_options(self, args: list[str]) -> list[str]:
        option: list[str] = []
        for arg in args:
            if arg.startswith("-"):
                option.append(arg.strip("-"))
        return option

    def extract_paths(self, args: list[str]) -> list[str]:
        paths = []
        for arg in args:
            if "/" in arg:
                paths.append(arg)
        return paths

    def _l(self, paths: list[str]) -> None:
        """
        List files in long format.
        """
        self.file_system

        for path in paths:
            print(f"Long format for {path}")
