import shutil
import os

FAKE_ROOT = './fake_root'

# Directory structure to create
directories = [
    'bin',
    'etc/network',
    'proc/net',
    'proc/sys/net/ipv4/conf/eth0',
    'sys/class/net/eth0/statistics',
    'sys/class/net/wlan0/statistics',
    'var/log'
]

# Files with example content
files = {
    'etc/hostname': 'honeypot-host\n',
    'etc/hosts': '127.0.0.1   localhost\n192.168.1.10 honeypot-host.localdomain honeypot-host\n',
    'etc/network/interfaces': """auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.1.10
    netmask 255.255.255.0
    gateway 192.168.1.1
""",
    'etc/resolv.conf': 'nameserver 8.8.8.8\n',
    'proc/net/dev': """Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
  eth0: 1234567  1234    0    0    0    0     0          0       2345678  2345    0    0    0     0       0          0
""",
    'proc/net/route': "Iface   Destination Gateway     Flags RefCnt Use Metric Mask        MTU Window IRTT\neth0    00000000    C0A80101    0003  0      0   100    00000000     0   0      0\n",
    'proc/net/arp': "IP address       HW type     Flags       HW address            Mask     Device\n192.168.1.1      0x1         0x2         00:11:22:33:44:55     *        eth0\n",
    'sys/class/net/eth0/address': '00:11:22:33:44:55\n',
    'sys/class/net/eth0/operstate': 'up\n',
    'sys/class/net/eth0/speed': '1000\n',
    'sys/class/net/eth0/statistics/rx_bytes': '123456789\n',
    'sys/class/net/eth0/statistics/tx_bytes': '987654321\n',
    'sys/class/net/wlan0/statistics/rx_bytes': '0\n',
    'sys/class/net/wlan0/statistics/tx_bytes': '0\n',
    'proc/sys/net/ipv4/conf/eth0/address': '192.168.1.10\n',
    'proc/sys/net/ipv4/conf/eth0/netmask': '255.255.255.0\n',
    'proc/sys/net/ipv4/conf/eth0/broadcast': '192.168.1.255\n',
    'var/log/messages.log': '[INFO] Network initialized on eth0\n',
}

def create_directory_structure(base_path):
    for directory in directories:
        path = os.path.join(base_path, directory)
        os.makedirs(path, exist_ok=True)
        # Suppress output

def populate_files(base_path):
    for rel_path, content in files.items():
        full_path = os.path.join(base_path, rel_path)
        dir_path = os.path.dirname(full_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        # Suppress output

def is_net_tools_installed():
    # Check if typical net-tools binaries exist
    tools = ['ifconfig', 'netstat', 'route', 'arp']
    return any(shutil.which(tool) for tool in tools)

# --- Fake Network Interface Definitions ---

class FakeInterface:
    def __init__(self, name, ip=None, netmask=None, broadcast=None,
                 status='down', mac='00:00:00:00:00:00', mtu=1500,
                 promisc=False, multicast=True):
        self.name = name
        self.ip = ip
        self.netmask = netmask
        self.broadcast = broadcast
        self.status = status
        self.mac = mac
        self.mtu = mtu
        self.promisc = promisc
        self.multicast = multicast

    def is_up(self):
        return self.status == 'up'

    def set_ip(self, ip):
        self.ip = ip

    def set_netmask(self, netmask):
        self.netmask = netmask

    def set_broadcast(self, broadcast):
        self.broadcast = broadcast

    def set_mac(self, mac):
        self.mac = mac

    def to_string(self):
        lines = [f"{self.name}: flags={'UP' if self.is_up() else 'DOWN'}"]
        lines.append(f"    inet {self.ip}  netmask {self.netmask}  broadcast {self.broadcast}" if self.ip else "    inet not assigned")
        lines.append(f"    ether {self.mac}  txqueuelen 1000  (Ethernet)")
        lines.append(f"    mtu {self.mtu}  {'PROMISC' if self.promisc else ''} {'MULTICAST' if self.multicast else ''}".strip())
        return '\n'.join(lines)

# --- Simulated Network Directory ---

fake_net_interfaces = {
    "eth0": FakeInterface(
        name="eth0",
        ip="192.168.1.10",
        netmask="255.255.255.0",
        broadcast="192.168.1.255",
        status="up",
        mac="00:11:22:33:44:55",
        mtu=1500,
        promisc=False
    ),
    "eth1": FakeInterface(
        name="eth1",
        ip=None,
        netmask=None,
        broadcast=None,
        status="down",
        mac="00:11:22:33:44:66",
        mtu=1500,
        promisc=False
    ),
    "lo": FakeInterface(
        name="lo",
        ip="127.0.0.1",
        netmask="255.0.0.0",
        broadcast=None,
        status="up",
        mac="00:00:00:00:00:00",
        mtu=65536,
        promisc=False
    ),
}

# --- Command Handlers ---

def ifconfig(args=None):
    """
    Simulates `ifconfig`, `ifconfig -a`, `ifconfig <interface>`, and
    `ifconfig <interface> <IP>`, `ifconfig <interface> netmask <mask>`, `ifconfig <interface> broadcast <address>`,
    `ifconfig <interface> hw ether <MAC>`.
    """
    if args is None or len(args) == 0:
        interfaces = [iface for iface in fake_net_interfaces.values() if iface.is_up()]
        return "\n\n".join(iface.to_string() for iface in interfaces)
    elif args[0] == '-a':
        interfaces = list(fake_net_interfaces.values())
        return "\n\n".join(iface.to_string() for iface in interfaces)
    else:
        name = args[0]
        iface = fake_net_interfaces.get(name)
        if not iface:
            return f"ifconfig: interface '{name}' not found"
        # Handle set IP/netmask/broadcast/hw ether
        if len(args) == 2:
            iface.set_ip(args[1])
            return iface.to_string()
        elif len(args) == 3:
            if args[1] == "netmask":
                iface.set_netmask(args[2])
                return iface.to_string()
            elif args[1] == "broadcast":
                iface.set_broadcast(args[2])
                return iface.to_string()
            else:
                return f"ifconfig: unknown option '{args[1]}'"
        elif len(args) == 4:
            if args[1] == "hw" and args[2] == "ether":
                iface.set_mac(args[3])
                return iface.to_string()
            else:
                return f"ifconfig: unknown option '{' '.join(args[1:])}'"
        else:
            return iface.to_string()

# --- Test Cases ---

def run_ifconfig_tests():
    print("===== ifconfig (default) =====")
    print(ifconfig())
    print("\n===== ifconfig -a =====")
    print(ifconfig(['-a']))
    print("\n===== ifconfig eth0 =====")
    print(ifconfig(['eth0']))
    print("\n===== ifconfig eth1 =====")
    print(ifconfig(['eth1']))
    print("\n===== ifconfig lo =====")
    print(ifconfig(['lo']))
    print("\n===== ifconfig invalid0 =====")
    print(ifconfig(['invalid0']))
    print("\n===== ifconfig eth0 10.0.0.5 =====")
    print(ifconfig(['eth0', '10.0.0.5']))
    print("\n===== ifconfig eth0 netmask 255.255.0.0 =====")
    print(ifconfig(['eth0', 'netmask', '255.255.0.0']))
    print("\n===== ifconfig eth0 broadcast 10.0.0.255 =====")
    print(ifconfig(['eth0', 'broadcast', '10.0.0.255']))
    print("\n===== ifconfig eth1 172.16.0.2 =====")
    print(ifconfig(['eth1', '172.16.0.2']))
    print("\n===== ifconfig eth1 netmask 255.255.255.128 =====")
    print(ifconfig(['eth1', 'netmask', '255.255.255.128']))
    print("\n===== ifconfig eth1 broadcast 172.16.0.255 =====")
    print(ifconfig(['eth1', 'broadcast', '172.16.0.255']))
    print("\n===== ifconfig lo 127.0.0.2 =====")
    print(ifconfig(['lo', '127.0.0.2']))
    print("\n===== ifconfig lo netmask 255.0.0.1 =====")
    print(ifconfig(['lo', 'netmask', '255.0.0.1']))
    print("\n===== ifconfig lo broadcast 127.255.255.255 =====")
    print(ifconfig(['lo', 'broadcast', '127.255.255.255']))
    print("\n===== ifconfig eth0 hw ether 12:34:56:78:9a:bc =====")
    print(ifconfig(['eth0', 'hw', 'ether', '12:34:56:78:9a:bc']))
    print("\n===== ifconfig eth1 hw ether aa:bb:cc:dd:ee:ff =====")
    print(ifconfig(['eth1', 'hw', 'ether', 'aa:bb:cc:dd:ee:ff']))
    print("\n===== ifconfig lo hw ether 00:00:00:00:00:01 =====")
    print(ifconfig(['lo', 'hw', 'ether', '00:00:00:00:00:01']))

# --- Main Execution ---

if __name__ == "__main__":
    # Setup fake honeypot environment (silent)
    create_directory_structure(FAKE_ROOT)
    populate_files(FAKE_ROOT)

    # Check net-tools and run ifconfig stub
    if is_net_tools_installed():
        print("net-tools is installed")
    else:
        print("net-tools is not installed")

    # Run ifconfig test cases
    run_ifconfig_tests()