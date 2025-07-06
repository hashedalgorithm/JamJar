from utils import helper
from utils.logger import Logger
from utils.parser import CommandParser

from commands.network.arp import ARP
from commands.network.ifconfig import IFCONFIG
from commands.network.ftp import FTP
from commands.network.ip import IP
from commands.network.nmap import NMAP
from commands.network.ping import PING
from commands.network.traceroute import TRACEROUTE


class NetworkHandler(Logger):
    def __init__(self) -> None:
        super().__init__()
        self.interfaces = helper.create_fake_interface_data_helper()
        self.arp_table = helper.create_fake_arp_data_helper(self.interfaces["ens18"])
        self.routes = helper.create_fake_route_data_helper(self.interfaces["ens18"])
        self.parser = CommandParser()
        self.command_options_map = {
            "ping": ["-c", "-I", "-i", "-l", "-m", "-p", "-Q", "-s", "-S", "-t", "-w", "-W"],
            "nmap": [],
            "ftp": ["-o", "-P", "-s", "-T", "-u", "-x"],
            "ip": ["-i", "-f"],
            "traceroute": ["-p", "-m", "-f", "-q", "-z"],
            "ifconfig": ["netmask", "broadcast", "mtu"], 
            "arp": ["-i", "-H", "-A", "-s", "-d"]
        }


    def handle(self, command: str, full_command: str):
        self.parser.set_options_with_values(self.command_options_map.get(command, []))
        parsed = self.parser.parse(full_command)
        match command:
            case "ifconfig":
                ifconfig = IFCONFIG(parsed)
                return ifconfig.run()

            case "nmap":
                nmap = NMAP(parsed)
                return nmap.run()

            case "ping":
                ping = PING(self.arp_table, self.interfaces, parsed)
                return ping.run()

            case "arp":
                arp = ARP(self.arp_table, parsed)
                return arp.run()

            case "ip":
                ip = IP(self.interfaces, self.routes, parsed)
                return ip.run()

            case "traceroute":
                traceroute = TRACEROUTE(self.interfaces, parsed)
                return traceroute.run()

            case "ftp":
                ftp = FTP(parsed)
                return ftp.run()

            case _:
                self.logger.info(
                    f"Command '{command}' not recognized by NetworkHandler."
                )
                return None
