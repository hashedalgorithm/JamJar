from commands.base import CommandBase
from models.arp import ARP
from models.interface import INTERFACE
from utils import helper
import random
import ipcalc


class PING(CommandBase):
    def __init__(self) -> None:
        super().__init__("ping")
        self.LOCAL_NETS = ["10.0.0.0/8", "172.16.0.0/12", "12.168.0.0/16"]

    def run(self) -> str | None:
        raise Exception("PING not implemented yet!")
    
    def ping(self, args):
        output = []

        target_host, _ = helper.get_main_arg_helper(args)
        target_ip = ""

        target_ip = helper.nslookup_helper(target_host)

        local = False
        if target_host not in self.arp_table:
            for net in self.LOCAL_NETS:
                if target_ip in ipcalc.Network(net):
                    local = True

            interface = self.interfaces["ens18"]
            arp_ip = target_ip if local else interface.inet4_gtw[0]

            self.arp_table[target_ip] = ARP(
                address=arp_ip, hwaddress="16:38:fd:f6:c2:c3", iface=interface
            )

        output.append(f"PING {target_host} ({target_ip}) 56(84) bytes of data.")
        time_total = 0

        for i in range(1, 5):
            time = str(random.randint(10, 50))
            time_dec = str(random.randint(1, 9))
            time_total += float(time + "." + time_dec)
            output.append(
                f"64 bytes from {target_ip}: icmp_seq={i} ttl=56 time={time}.{time_dec} ms"
            )

        output.append(f"--- {target_host} ping statistics ---")
        output.append(
            f"4 packets transmitted, 4 received, 0% packet loss, time {time_total}"
        )
        output.append("rtt min/avg/max/mdev = 12.578/13.047/13.555/0.273 ms")

        return output