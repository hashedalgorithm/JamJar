from typing import Literal


class NetworkInterface:
    """
    A class to represent a network interface with all relevant options.
    """

    def __init__(
        self,
        name: str,
        mac_address: str,
        id: int,
        flags: str,
        type: Literal[
            "eth",  # Ethernet interface
            "enp0s1",  # Specific Ethernet interface (modern naming convention)
            "wlan",  # Wireless interface
            "lo",  # Loopback interface
            "wwan",  # Cellular interface
            "br",  # Bridge interface
            "tun",  # Tunnel interface
            "tap",  # TAP interface
            "veth",  # Virtual Ethernet interface
            "virbr",  # Virtual bridge interface
            "ppp",  # Point-to-Point Protocol interface
            "bond",  # Bonded interface
            "vxlan",  # VXLAN interface
            "gre",  # GRE tunnel interface
            "hci",  # Bluetooth interface
            "docker",  # Docker container interface
            "ovs",  # Open vSwitch interface
            "usb",  # USB network interface
            "sfp",  # Fiber optic interface
        ],
        status: Literal["down", "up"] = "down",
        mtu: int = 1500,
        rx_packets: int = 0,
        tx_packets: int = 0,
        rx_bytes: int = 0,
        tx_bytes: int = 0,
        rx_errors: int = 0,
        tx_errors: int = 0,
        ipv4_address: str = None,
        netmask: str = None,
        broadcast: str = None,
        ipv6_addresses: list = None,
        txqueuelen: int = 1000,
        rx_dropped: int = 0,
        rx_overruns: int = 0,
        rx_frame: int = 0,
        tx_dropped: int = 0,
        tx_overruns: int = 0,
        tx_carrier: int = 0,
        tx_collisions: int = 0,
    ):
        self.name = name
        self.flags = flags
        self.id = id
        self.type = type
        self.mac_address = mac_address
        self.status = status
        self.mtu = mtu
        self.rx_packets = rx_packets
        self.tx_packets = tx_packets
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.rx_errors = rx_errors
        self.tx_errors = tx_errors
        self.ipv4_address = ipv4_address
        self.netmask = netmask
        self.broadcast = broadcast
        self.ipv6_addresses = ipv6_addresses or []
        self.txqueuelen = txqueuelen
        self.rx_packets = rx_packets
        self.rx_bytes = rx_bytes
        self.rx_errors = rx_errors
        self.rx_dropped = rx_dropped
        self.rx_overruns = rx_overruns
        self.rx_frame = rx_frame
        self.tx_packets = tx_packets
        self.tx_bytes = tx_bytes
        self.tx_errors = tx_errors
        self.tx_dropped = tx_dropped
        self.tx_overruns = tx_overruns
        self.tx_carrier = tx_carrier
        self.tx_collisions = tx_collisions

    def __repr__(self):
        """
        Generate a string representation of the network interface.
        """
        ipv4_info = (
            f"        inet {self.ipv4_address}  netmask {self.netmask}  broadcast {self.broadcast}\n"
            if self.ipv4_address and self.netmask and self.broadcast
            else ""
        )

        ipv6_info = "\n".join(
            [
                f"        inet6 {addr['address']}  prefixlen {addr['prefixlen']}  scopeid {addr['scopeid']}"
                for addr in self.ipv6_addresses
            ]
        )

        mac_info = (
            f"        ether {self.mac_address}  txqueuelen {self.txqueuelen}  (Ethernet)\n"
            if self.mac_address
            else ""
        )

        rx_info = (
            f"        RX packets {self.rx_packets}  bytes {self.rx_bytes} ({self.rx_bytes / (1024**2):.1f} MB)\n"
            f"        RX errors {self.rx_errors}  dropped {self.rx_dropped}  overruns {self.rx_overruns}  frame {self.rx_frame}\n"
        )

        tx_info = (
            f"        TX packets {self.tx_packets}  bytes {self.tx_bytes} ({self.tx_bytes / (1024**2):.1f} MB)\n"
            f"        TX errors {self.tx_errors}  dropped {self.tx_dropped}  overruns {self.tx_overruns}  carrier {self.tx_carrier}  collisions {self.tx_collisions}\n"
        )

        return (
            f"{self.name}: flags={self.flags}  mtu {self.mtu}\n"
            f"{ipv4_info}"
            f"{ipv6_info}\n"
            f"{mac_info}"
            f"{rx_info}"
            f"{tx_info}"
        )

    def bring_up(self):
        """
        Bring the network interface up.
        """
        self.status = "up"

    def bring_down(self):
        """
        Bring the network interface down.
        """
        self.status = "down"

    def reset_statistics(self):
        """
        Reset the packet and byte statistics for the interface.
        """
        self.rx_packets = 0
        self.tx_packets = 0
        self.rx_bytes = 0
        self.tx_bytes = 0
        self.rx_errors = 0
        self.tx_errors = 0
        self.rx_dropped = 0
        self.rx_overruns = 0
        self.rx_frame = 0
        self.tx_dropped = 0
        self.tx_overruns = 0
        self.tx_carrier = 0
        self.tx_collisions = 0
