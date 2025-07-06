from commands.base import CommandBase
from utils import helper
from models.file import File


class TOUCH(CommandBase):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> str | None:
        raise Exception("TOUCH not implemented yet!")
    
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