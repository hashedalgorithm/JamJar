from pwd import getpwuid

UserGroups = dict[str, int]


DEFAULT_USER_GROUPS = {
    "adm": 4,
    "cdrom": 24,
    "sudo": 27,
    "dip": 30,
    "plugdev": 46,
    "users": 100,
    "lpadmin": 114,
}


class User:
    def __init__(
        self,
        uid: int,
        gid: int | None = None,
        username: str | None = None,
        groups: UserGroups = DEFAULT_USER_GROUPS,
    ):
        self.uid: int = uid
        self.gid: int = gid if gid else getpwuid(uid).pw_gid
        self.username: str = username if username else self.get_username_by_uid(uid)
        self.groups: dict[str, int] = groups
        self.groups[username] = uid

    def get_username_by_uid(self, uid):
        try:
            return getpwuid(uid).pw_name
        except KeyError:
            return None

    def get_gid_by_uid(self, uid):
        try:
            return getpwuid(uid).pw_gid
        except KeyError:
            return None

    def __repr__(self):
        return f"{self.username}({self.uid})"


class Users:
    def __init__(self, users: dict[int, User] = {}):
        self.users = users

    def get(self, uid: int) -> User | None:
        return self.users.get(uid)

    def add(self, user: User) -> None:
        if self.get(user.uid):
            raise ValueError(f"User with UID '{user.uid}' already exists!")

        self.users[user.uid] = user

    def delete(self, uid: int) -> None:

        if not self.get(uid):
            raise ValueError(f"User with UID '{uid}' does not exist!")

        del self.users[uid]

    def is_exists(self, uid: int) -> bool:
        user = self.get(uid)

        return bool(user)

    def list_uid(self) -> list[int]:
        return [user.uid for user in self.users.values()]

    def __repr__(self):
        return f"Users({', '.join([repr(user) for user in self.users.values()])})"
