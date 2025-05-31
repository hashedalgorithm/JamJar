from utils import helper
from models.storage_entry import StorageEntry


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class DIR_handler:

    def __init__(self) -> None:
        self.root = helper.create_fake_dir_data_helper()

    def command_handler(self, cmd: str, src_dir: str = ""):
        output = None

        cmd_name = cmd.split(" ")[0]
        args = cmd.split(" ")[1:]

        match cmd_name:

            case "ls":
                output = self.ls(args, src_dir)

            case "rm":
                output = self.rm(args, src_dir)

            case "touch":
                output = self.touch(args, src_dir)

        return output

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

        target_obj = StorageEntry(target_file, file_type=file_type)

        helper.add_file_helper(
            self.root, src_dir_list if path_flag else src_dir, target_obj
        )

        return None
