from utils import helper
from models.storage_entry import StorageEntry
from models.util import bcolors


class DirectoryHandler:

    def __init__(self) -> None:
        self.root = helper.create_fake_dir_data_helper()

    def handle(self, cmd: str, src_dir: str = "") -> str | None:

        cmd_name = cmd.split(" ")[0]
        args = cmd.split(" ")[1:]

        match cmd_name:
            case "cd":
                return self.cd(args)

            case "ls":
                return self.ls(args, src_dir)

            case "rmdir":
                return self.rmdir()

            case "mkdir":
                return self.mkdir()

            case "mv":
                return self.mv()

            case "cp":
                return self.cp()

            case "rm":
                return self.rm(args, src_dir)

            case _:
                print(f"Command '{cmd}' not recognized by DirectoryHandler.")
                return None

    def cd(self):
        # TODO: Implement cd command
        print("cd not implemented yet")
        return None

    def ls(self, args: str, src_dir: str):
        output = ""
        target_dir = ""
        src_dir_list = helper.path_to_list_helper(src_dir)

        option, args_str = helper.get_main_arg_helper(args)
        striped_option = option.strip("-")

        print(striped_option, args_str)

        target_dir, args_str = helper.get_main_arg_helper(args)

        if "/" in target_dir:
            target_dir, src_dir_list = helper.target_dir_is_path_helper(
                target_dir, helper.path_to_list_helper(src_dir_list)
            )

        src_obj = self.root

        if src_dir_list != []:
            for layer in src_dir_list:
                try:
                    src_obj = src_obj.content[layer]
                except KeyError:
                    return f"ls: cannot access '{src_dir}': No such file or directory"

        if target_dir:
            try:
                target_obj = src_obj.content[target_dir]
            except KeyError:
                return f"ls: cannot access '{target_dir}': No such file or directory"
        else:
            target_obj = src_obj

        if target_obj.file_type != "directory":
            output = target_obj.name

        else:
            l = "l" in args_str
            a = "a" in args_str
            r = "r" in args_str

            if l:
                target_obj_parent = target_obj.parent
                output += f"{target_obj.perm} {target_obj.xxx} {target_obj.owner} {target_obj.group} {target_obj.size} {target_obj.created_month} {target_obj.created_day} {target_obj.created_time} "
                output += bcolors.OKBLUE + f"{'.'}\n" + bcolors.ENDC

                output += f"{target_obj_parent.perm} {target_obj_parent.xxx} {target_obj_parent.owner} {target_obj_parent.group} {target_obj_parent.size} {target_obj_parent.created_month} {target_obj_parent.created_day} {target_obj_parent.created_time} "
                output += bcolors.OKBLUE + f"{'..'}\n" + bcolors.ENDC

            for file in target_obj.content:
                print_obj = target_obj.content[file]
                is_dir = print_obj.file_type == "directory"

                if not a and file.startswith("."):
                    continue

                if l:
                    output += f"{print_obj.perm} {print_obj.xxx} {print_obj.owner} {print_obj.group} {print_obj.size} {print_obj.created_month} {print_obj.created_day} {print_obj.created_time} "

                    if is_dir:
                        output += bcolors.OKBLUE
                    output += f"{file}\n"
                    if is_dir:
                        output += bcolors.ENDC

                else:
                    if is_dir:
                        output += bcolors.OKBLUE
                    output += file + " "
                    if is_dir:
                        output += bcolors.ENDC

            output = output.strip("\n ")

            if r:
                output_list = output.split("\n" if l else " ")
                output_list.reverse()

                join_char = "\n" if l else " "
                output = join_char.join(output_list)

                # TODO Temp fix for color magic bytes being reversed
                output = output.replace(bcolors.OKBLUE, "")
                output = output.replace(bcolors.ENDC, "")

        return output

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

    def rm(self, args, src_dir):
        target_file = ""
        src_dir_list = helper.path_to_list_helper(src_dir)

        target_file, args_str = helper.get_main_arg_helper(args)

        if "/" in target_file:
            target_file, src_dir_list = helper.target_dir_is_path_helper(
                target_file, src_dir_list
            )

        if not target_file:
            output = "rm: missing operand \nTry 'rm --help' for more information."
            return output

        src_obj = self.root

        if src_dir_list != []:
            for layer in src_dir_list:
                src_obj = src_obj.content[layer]

        try:
            target_obj = src_obj.content[target_file]
        except KeyError:
            return f"rm: cannot remove '{target_file}': No such file or directory"

        r = "r" in args_str
        f = "f" in args_str

        if not r and target_obj.file_type == "directory":
            return

        src_obj.content.pop(target_file)

        return None
