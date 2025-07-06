from commands.base import CommandBase
from utils import helper
from models.arp import ARP


class ARP(CommandBase):
    def __init__(self) -> None:
        super().__init__("arp")

    def run(self) -> str | None:
        raise Exception("ARP not implemented yet!")
    
    def arp(self, args):
        output = None

        target_host, args_str = helper.get_main_arg_helper(args)

        d = "d" in args_str

        if d:
            if not target_host:
                return "arp: need host name"

            if not target_host in self.arp_table:
                return f"{target_host}: No address associated with name"

            self.arp_table.pop(target_host)

        else:
            output = "Address\t\tHWtype\t\tHWaddress\t\tFlags Mask\tIface\n"
            for entry in self.arp_table:
                output += str(self.arp_table[entry]) + "\n"

        return output