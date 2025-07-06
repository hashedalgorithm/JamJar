from commands.base import CommandBase
from utils import helper
from models.interface import INTERFACE
import random
from utils.parser import ParsedCommand


class TRACEROUTE(CommandBase):
    def __init__(self, parsed: ParsedCommand) -> None:
        super().__init__("traceroute")
        self.parsed = parsed
        
    def run(self) -> str | None:
        raise Exception("TRACEROUTE not implemented yet!")
    
    def traceroute(self, args):
        output = []
        target_ip = ""

        target_host, _ = helper.get_main_arg_helper(args)
        target_ip = helper.nslookup_helper(target_host)

        output.append(f"traceroute to {target_host} ({target_ip}), 64 hops max")

        random_hops = random.randint(5, 11)

        for i in range(1, random_hops):
            time_total = []
            for _ in range(3):
                time = str(random.randint(1 * (i - 1), 10 * (i - 1)))
                time_dec = str(random.randint(1, 9))

                time_total.append(str(float(time + "." + time_dec)) + "ms")

            interface = self.interfaces["ens18"]

            if i == 1:
                ip = interface.inet4_gtw[0]
            elif i == random_hops - 1:
                ip = target_ip
            else:
                ip = random.choice(helper.TRACEROUTES)

            output.append(f"{i}  {ip} {" ".join(time_total)}")

        return output