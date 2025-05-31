from models.storage_entry import StorageEntry
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


def path_to_list_helper(path: str) -> list:
    return path.strip("/").split("/") if path != "/" and path != "" else []


def get_main_arg_helper(args: list) -> tuple:
    target = ""

    for arg in args:
        if not arg.startswith("-"):
            target = arg
            args.remove(arg)  # Call by reference hat auch Vorteile :D
            break
    return target, "".join(args)


def add_file_helper(root: StorageEntry, path_list: list, data: StorageEntry | File):

    parent = root

    for layer in path_list:
        # accessing the folder/file
        parent = parent.content[layer]

    data.parent = parent
    parent.content[data.name] = data


def target_dir_is_path_helper(target_dir: str, src_dir_list: list):
    if target_dir.startswith("/"):
        src_dir_list_tmp = path_to_list_helper(target_dir)
        src_dir_list = src_dir_list_tmp[:-1]
        target_dir = src_dir_list_tmp[-1]
    else:
        split = target_dir.split("/")
        src_dir_list = src_dir_list + split[:-1]
        target_dir = split[-1]

    return target_dir, src_dir_list


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


def create_fake_dir_data_helper() -> StorageEntry:
    username = get_username_by_uid() or "user"

    root_start = ["bin", "dev", "etc", "usr", "home", "lib", "sbin", "tmp", "var"]

    home_user = [
        ["file", ".bash_history", "", "-rw-------", "Jul", "13", "12:31"],
        ["file", ".bash_logout", "", "-rw-r--r--", "Jul", "13", "12:31"],
        ["dir", ".cache", "", "drwx------", "May", "20", "21:13"],
        ["file", ".bashrc", "", "drwx------", "May", "20", "21:13"],
        ["dir", ".local", "", "drwxrwxr-x", "Jul", "1", "00:25"],
        ["file", ".profile", "", "-rw-r--r--", "Jul", "7", "14:10"],
        ["dir", ".ssh", "", "drwx------", "Jun", "13", "19:14"],
        ["file", "test_file", "txt", "-rw-r--r--", "Jun", "15", "11:12"],
        ["file", ".test_file_hidden", "txt", "-rw-r--r--", "Jun", "15", "11:13"],
    ]

    root = StorageEntry("root", file_type="directory", perm="drwxrwxrwx")
    root.parent = root

    for dir in root_start:
        add_file_helper(
            root,
            path_to_list_helper("/"),
            StorageEntry(
                dir,
                file_type="directory",
                perm="drwxr-xr-x",
                created_month="Jul",
                created_day=11,
                created_time="12:29",
            ),
        )

    add_file_helper(
        root,
        path_to_list_helper("/home"),
        StorageEntry(username, file_type="directory", perm="drwxr-x---"),
    )
    for file in home_user:

        add_file_helper(
            root,
            path_to_list_helper(f"/home/{username}/"),
            (
                StorageEntry(
                    name=file[1],
                    file_type=(
                        "directory"
                        if file[0] == "dir"
                        else "file" if not file[2] else file[2]
                    ),
                    perm=file[3],
                    created_month=file[4],
                    created_day=file[5],
                    created_time=file[6],
                    owner=username,
                    group=username,
                )
            ),
        )

    # TODO more fake dirs

    return root


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
