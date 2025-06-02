from utils import helper 
from utils import parser
from models.file_system import FileSystem


class DirectoryHandler:

    def __init__(self) -> None:
        self.file_system = FileSystem()

    def handle(self, cmd: str, src_dir: str = "") -> str | None:

        cmd_name = cmd.split(" ")[0]
        args = cmd.split(" ")[1:]
        match cmd_name:
            case "cd":
                return self.cd()

            case "ls":
                return self.ls()

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
                print(f"Command '{cmd}' not recognized by DirectoryHandler.")
                return None

    def cd(self):
        # TODO: Implement cd command
        print("cd not implemented yet")
        return None


    def ls(self):
        # TODO: Implement ls command
        print("ls not implemented yet")
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
    
if __name__ == "__main__":
    DH = DirectoryHandler()
    command:str = input("Enter command: ")
    print(DH.handle(command))
