from utils import helper
from models.file import File


class FileOpsHandler:
    def __int__(self):
        pass

    def handle(self, command: str, args: list[str]):

        match command:
            case "touch":
                return self.touch(args, "")

            case "cat":
                return self.cat()

            case "grep":
                return self.grep()

            case "echo":
                return self.echo()

            case "locate":
                return self.locate()

            case "wget":
                return self.wget()

            case "curl":
                return self.curl()

            case "unzip":
                return self.unzip()

            case "chmod":
                return self.chmod()

            case "nano":
                return self.nano()

            case "pico":
                return self.pico()

            case "vi":
                return self.vi()

            case "vim":
                return self.vim()

            case "ln":
                return self.ln()

            case "crontab":
                return self.crontab()

            case _:
                print(f"Command '{command}' not recognized by FileOpsHandler.")
                return None

    def touch(self, args, src_dir):
        target_file = ""
        path_flag = False

        target_file, _ = helper.get_main_arg_helper(args)

        if "/" in target_file:
            path_flag = True
            target_file, src_dir_list = helper.target_dir_is_path_helper(
                target_file, src_dir
            )

        if not target_file:
            output = (
                "touch: missing file operand \nTry 'touch --help' for more information."
            )
            return output

        file_type_split = target_file.split(".")

        if len(file_type_split) > 1:
            file_type = target_file.split(".")[-1]
        else:
            file_type = "file"

        target_obj = File(target_file, file_type=file_type)

        helper.add_file_helper(
            self.root, src_dir_list if path_flag else src_dir, target_obj
        )

        return None

    def cat(self) -> str | None:
        # TODO: Implement cat command
        print("cd not implemented yet")
        return None

    def grep(self) -> str | None:
        # TODO: Implement grep command
        print("grep not implemented yet")
        return None

    def echo(self) -> str | None:
        # TODO: Implement echo command
        print("echo not implemented yet")
        return None

    def locate(self) -> str | None:
        # TODO: Implement locate command
        print("locate not implemented yet")
        return None

    def wget(self) -> str | None:
        # TODO: Implement wget command
        print("wget not implemented yet")
        return None

    def curl(self) -> str | None:
        # TODO: Implement curl command
        print("curl not implemented yet")
        return None

    def unzip(self) -> str | None:
        # TODO: Implement unzip command
        print("unzip not implemented yet")
        return None

    def chmod(self) -> str | None:
        # TODO: Implement chmod command
        print("chmod not implemented yet")
        return None

    def nano(self) -> str | None:
        # TODO: Implement nano command
        print("nano not implemented yet")
        return None

    def pico(self) -> str | None:
        # TODO: Implement pico command
        print("pico not implemented yet")
        return None

    def vi(self) -> str | None:
        # TODO: Implement vi command
        print("vi not implemented yet")
        return None

    def vim(self) -> str | None:
        # TODO: Implement vim command
        print("vim not implemented yet")
        return None

    def ln(self) -> str | None:
        # TODO: Implement ln command
        print("ln not implemented yet")
        return None

    def crontab(self) -> str | None:
        # TODO: Implement crontab command
        print("crontab not implemented yet")
        return None
