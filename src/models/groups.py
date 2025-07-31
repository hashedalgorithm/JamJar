from pwd import getpwuid
from grp import getgrgid

DEFAULT_USER_GROUPS = {
    "adm": 4,
    "cdrom": 24,
    "sudo": 27,
    "dip": 30,
    "plugdev": 46,
    "users": 100,
    "lpadmin": 114,
}


class Group:
    def __init__(self, uid: int = None, gid: int = None, group_username: str = None):
        if uid and not gid and not group_username:
            self.__init_by_uid__(uid)
            return

        if not uid and gid and group_username:
            self.__init_by_gid__(gid, group_username)
            return

        raise ValueError("Initalize Group by either only uid or gid and group username")

    def __init_by_uid__(self, uid: int):
        self.gid: int = self.get_gid_by_uid(uid)
        self.group_username: str = getgrgid(self.gid).gr_name

    def __init_by_gid__(self, gid: int, group_username: str):
        self.gid: int = gid
        self.group_username: str = group_username

    def get_gid_by_uid(self, uid):
        try:
            return getpwuid(uid).pw_gid
        except KeyError:
            return None

    def __repr__(self):
        return f"Group:(gid: {self.gid}; g_username: {self.group_username})"


class Groups:
    def __init__(self):
        self.groups: dict[int, Group] = {}

        for group_username, gid in DEFAULT_USER_GROUPS.items():
            self.add_group(Group(gid=gid, group_username=group_username))

    def get_group(self, gid: int) -> Group | None:
        return self.groups.get(gid)

    def add_group(self, group: Group) -> None:
        if self.get_group(group.gid):
            raise ValueError(f"Group with GID '{group.gid}' already exists!")

        self.groups[group.gid] = group

    def delete_group(self, gid: int) -> None:

        if not self.get_group(gid):
            raise ValueError(f"User with UID '{gid}' does not exist!")

        del self.groups[gid]

    def is_group_exists(self, gid: int) -> bool:
        group = self.get_group(gid)

        return bool(group)

    def list_gid(self) -> list[int]:
        return [group.gid for group in self.groups.values()]

    def __repr__(self):
        return f"Groups({', '.join([repr(group) for group in self.groups.values()])})"
