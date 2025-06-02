from models.arp import ARP
from models.route import ROUTE
from models.interface import INTERFACE
from models.process import Process

from pwd import getpwuid

import socket


TRACEROUTES = [
    "62.155.245.90",
    "217.5.70.26",
    "80.156.160.223",
    "80.231.65.10",
    "195.219.148.122",
    "162.158.84.111",
    "172.69.148.3",
]

def has_more_than_one_positional(arguments):
    count = sum(1 for arg in arguments if arg['type'] == 'positional')
    return count > 1

def path_to_cleaned_list(path: str) -> list[str]:
    if not path:
        return []

    is_absolute = path.startswith("/")
    components = path.split("/")

    result = []

    for comp in components:
        # Skip empty components caused by multiple slashes
        if comp == "" or comp == ".":
            continue
        elif comp == "..":
            if result and result[-1] != "/" and result[-1] != "..":
                result.pop()  # Cancel the last valid directory
            elif not is_absolute:
                result.append("..")  # Relative path: preserve leading ..
        else:
            result.append(comp)

    if is_absolute:
        result.insert(0, "/")

    return result

def get_main_arg_helper(args: list) -> tuple:
    target = ""

    for arg in args:
        if not arg.startswith("-"):
            target = arg
            args.remove(arg)  # Call by reference hat auch Vorteile :D
            break
    return target, "".join(args)


def nslookup_helper(domain):
    ip = ""

    if domain[0].isalpha():
        ip = socket.getaddrinfo(domain, 0)[0][4][0]
    else:
        ip = domain

    return ip


def get_username_by_uid(uid=1000):
    try:
        return getpwuid(uid).pw_name
    except KeyError:
        return None


def create_fake_arp_data_helper(int1):
    return {
        "_gateway": ARP(address="_gateway", hwaddress="af:33:4f:f6:2c:dd", iface=int1)
    }


def create_fake_interface_data_helper():
    return {
        "lo": INTERFACE(),
        "ens18": INTERFACE(
            ["ens18", "enp0s18"],
            "ether",
            1500,
            "BROADCAST,MULTICAST",
            mac="42:f6:3a:54:ad",
            mac_brd="ff:ff:ff:ff:ff:ff",
            state=2,
            inet4=["192.168.0.12/24"],
            inet6="fe80::ef52:de12:d4ee:139a/64",
        ),
    }


def create_fake_route_data_helper(interface):
    return [
        ROUTE(inet_from="default", inet_to=interface.inet4_gtw[0], interface=interface)
    ]


def create_fake_processes():
    processes = [
        Process(
            pid=1,
            tty="?",
            time="00:00:09",
            cmd="systemd",
            uid="root",
            ppid="0",
            c="2503",
            stime="12:30",
            stat="Ss",
            sid="1",
            cpu="0.2",
            mem="0.0",
            rss="11888",
            vsz="170260",
            ucmd="/sbin/init splash",
        ),
        Process(
            2,
            "?",
            "00:00:00",
            "kthreadd",
            "root",
            "0",
            "0",
            "12:30",
            "S",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[kthreadd]",
        ),
        Process(
            3,
            "?",
            "00:00:00",
            "rcu_gp",
            "root",
            "0",
            "0",
            "12:30",
            "I<",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[rcu_gp]",
        ),
        Process(
            4,
            "?",
            "00:00:00",
            "rcu_par_gp",
            "root",
            "0",
            "0",
            "12:30",
            "I<",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[rcu_par_gp]",
        ),
        Process(
            5,
            "?",
            "00:00:00",
            "slub_flushwq",
            "root",
            "0",
            "0",
            "12:30",
            "I<",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[slub_flushwq]",
        ),
        Process(
            6,
            "?",
            "00:00:00",
            "netns",
            "root",
            "0",
            "0",
            "12:30",
            "I<",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[netns]",
        ),
        Process(
            8,
            "?",
            "00:00:00",
            "kworker/0:0H-events_highpri",
            "root",
            "0",
            "0",
            "12:30",
            "I<",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[kworker/0:0H-events_highpri]",
        ),
        Process(
            10,
            "?",
            "00:00:00",
            "mm_percpu_wq",
            "root",
            "0",
            "0",
            "12:30",
            "I<",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "[mm_percpu_wq]",
        ),
        Process(
            1673,
            "tty2",
            "00:00:00",
            "gdm-x-session",
            "user1",
            "0",
            "2503",
            "12:31",
            "S",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "/usr/lib/gdm3/gdm-x-session --run-script env GNOME_SHELL_SESSION_MODE=ubuntu",
        ),
        Process(
            1675,
            "tty2",
            "00:00:00",
            "Xorg",
            "user1",
            "0",
            "0",
            "12:32",
            "S",
            "0",
            "0.8",
            "0.0",
            "0",
            "0",
            "/usr/lib/xorg/Xorg vt2 -displayfd 3 -auth /run/user/1000/gdm/Xauthority -back",
        ),
        Process(
            1682,
            "tty2",
            "00:00:00",
            "gnome-keyring-d",
            "user1",
            "0",
            "0",
            "12:32",
            "S",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "/usr/libexec/gnome-session-binary --systemd -systemd -session=ubuntu",
        ),
        Process(
            2587,
            "pts/0",
            "00:00:00",
            "bash",
            "user1",
            "0",
            "0",
            "12:32",
            "S",
            "0",
            "0.0",
            "0.0",
            "0",
            "0",
            "bash",
        ),
    ]

    return processes
