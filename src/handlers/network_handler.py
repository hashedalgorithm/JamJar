from models.arp import ARP
from models.route import ROUTE
from utils import helper

import random
import ipcalc

LOCAL_NETS = ["10.0.0.0/8", "172.16.0.0/12", "12.168.0.0/16"]


class NETWORK_handler:

    output = None

    arp_table = {}
    interfaces = []

    def __init__(self) -> None:
        self.interfaces = helper.create_fake_interface_data_helper()
        self.arp_table = helper.create_fake_arp_data_helper(self.interfaces["ens18"])
        self.routes = helper.create_fake_route_data_helper(self.interfaces["ens18"])

    def cmd(self, cmd):
        output = None

        cmd_name = cmd.split(" ")[0]
        args = cmd.split(" ")[1:]

        match cmd_name:

            case "ping":
                output = self.ping(args)

            case "arp":
                output = self.arp(args)

            case "ip":
                output = self.ip(args)

            case "traceroute":
                output = self.traceroute(args)

        return output

    def ping(self, args):
        output = []

        target_host, _ = helper.get_main_arg_helper(args)
        target_ip = ""

        target_ip = helper.nslookup_helper(target_host)

        local = False
        if target_host not in self.arp_table:
            for net in LOCAL_NETS:
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

    def ip(self, args):

        output = ""

        args_str = "".join(args)
        a = "a" in args_str or "addr" in args_str
        r = "r" in args_str or "route" in args_str
        add = "add" in args_str
        delete = "del" in args_str

        if a:
            if add:
                self.interfaces[args[-1]].add_ip(args[-3])

            elif delete:
                self.interfaces[args[-1]].del_ip(args[-3])

            else:
                for n, entry in enumerate(self.interfaces):
                    output += f"{n+1}: {str(self.interfaces[entry])}\n"

        if r:
            if add:
                self.routes.append(
                    ROUTE(inet_to=args[-3], interface=self.interfaces[args[-1]])
                )

            elif delete:
                for x, route in enumerate(self.routes):
                    if args[-1] in route.interface.names and route.inet_to in args[-3]:
                        self.routes.pop(x)
                        break
            else:
                for entry in self.routes:
                    output += str(entry) + "\n"

        return output.strip("\n")

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
