from models.file_system import FileSystem
from utils.logger import Logger
from commands.ls import LS
from utils.parser import Parser


class DirectoryHandler(Logger):

    def __init__(self, file_system: FileSystem) -> None:
        super().__init__()
        self.file_system = file_system

    def handle(self, command: str, parsed_args: Parser) -> str | None:

        match command:
            case "cd":
                return self.cd()

            case "ls":
                ls = LS(self.file_system)
                return ls.run()

            case "rmdir":
                return self.rmdir()

            case "mkdir":
                return self.mkdir()

            case "mv":
                return self.mv()

            case "cp":
                return self.cp()

            case "rm":
                return self.rm()

            case _:
                print(f"Command '{command}' not recognized by DirectoryHandler.")
                return None

    def cd(self):
        # TODO: Implement cd command
        print("cd not implemented yet")
        return None

    def rmdir(self):
        # TODO: Implement rmdir command
        print("rmdir not implemented yet")
        return None

    def mkdir(self):
        # TODO: Implement mkdir command
        print("mkdir not implemented yet")
        return None

    def mv(self):
        # TODO: Implement mv command
        print("mv not implemented yet")
        return None

    def cp(self):
        # TODO: Implement cp command
        print("cp not implemented yet")
        return None

    def rm(self):
        # TODO: Implement rm command
        print("rm not implemented yet")
        return None
