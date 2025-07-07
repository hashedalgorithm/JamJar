from models.network_interface import NetworkInterface
from models.route import Route
from models.arp import ARP


class NetworkSystem:

    Traceroutes = [
        "62.155.245.90",
        "217.5.70.26",
        "80.156.160.223",
        "80.231.65.10",
        "195.219.148.122",
        "162.158.84.111",
        "172.69.148.3",
    ]

    def __init__(self):
        self.interfaces: dict[str, NetworkInterface] = {}

        self.create_fake_network_interfaces()
        self.arp_table = self.create_fake_arp_data_helper(self.interfaces["enp0s1"])
        self.routes = self.create_fake_route_data_helper(self.interfaces["enp0s1"])

    def create_fake_network_interfaces(self):

        self.interfaces["enp0s1"] = NetworkInterface(
            name="enp0s1",
            id=1,
            status="up",
            type="enp0s1",
            mac_address="6E:92:F4:3B:5A:C7",
            flags="4163<UP,BROADCAST,RUNNING,MULTICAST>",
            mtu=1500,
            ipv4_address="192.168.64.4",
            netmask="255.255.255.0",
            broadcast="192.168.64.255",
            ipv6_addresses=[
                {
                    "address": "fe80::883c:20ff:fea1:2a49",
                    "prefixlen": 64,
                    "scopeid": "0x20<link>",
                },
                {
                    "address": "fd8a:2ef5:3816:f3ad:1fe:d68d:52b0:22c1",
                    "prefixlen": 64,
                    "scopeid": "0x0<global>",
                },
                {
                    "address": "fd8a:2ef5:3816:f3ad:70ae:a50b:8718:f1d3",
                    "prefixlen": 64,
                    "scopeid": "0x0<global>",
                },
                {
                    "address": "fd8a:2ef5:3816:f3ad:883c:20ff:fea1:2a49",
                    "prefixlen": 64,
                    "scopeid": "0x0<global>",
                },
                {
                    "address": "fd8a:2ef5:3816:f3ad:f7a7:eb6f:500c:fcc5",
                    "prefixlen": 64,
                    "scopeid": "0x0<global>",
                },
            ],
            txqueuelen=1000,
            rx_packets=1249582,
            rx_bytes=1510717271,
            rx_errors=0,
            rx_dropped=0,
            rx_overruns=0,
            rx_frame=0,
            tx_packets=411355,
            tx_bytes=287499876,
            tx_errors=0,
            tx_dropped=0,
            tx_overruns=0,
            tx_carrier=0,
            tx_collisions=0,
        )
        self.interfaces["l0"] = NetworkInterface(
            name="l0",
            id=0,
            status="down",
            type="lo",
            mac_address="7F:01:G5:4C:6B:B8",
            flags="73<UP,LOOPBACK,RUNNING>",
            mtu=65536,
            ipv4_address="127.0.0.1",
            netmask="255.0.0.0",
            ipv6_addresses=[
                {"address": "::1", "prefixlen": 128, "scopeid": "0x10<host>"},
            ],
            txqueuelen=1000,
            rx_packets=36319,
            rx_bytes=5645729,
            rx_errors=0,
            rx_dropped=0,
            rx_overruns=0,
            rx_frame=0,
            tx_packets=36319,
            tx_bytes=5645729,
            tx_errors=0,
            tx_dropped=0,
            tx_overruns=0,
            tx_carrier=0,
            tx_collisions=0,
        )

    def create_fake_route_data_helper(self, interface: NetworkInterface):
        return [
            Route(
                inet_from="default",
                inet_to=interface.ipv4_address[0],
                interface=interface,
            )
        ]

    def create_fake_arp_data_helper(self, int1):
        return {
            "_gateway": ARP(
                address="_gateway", hwaddress="af:33:4f:f6:2c:dd", iface=int1
            )
        }
