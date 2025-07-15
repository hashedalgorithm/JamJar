from models.users import Users, User
from models.groups import Groups, Group


class UserManager(Users, Groups):
    def __init__(self):
        Users.__init__(self)
        Groups.__init__(self)
        self.whitelisted_users = []
        self.blacklisted_users = []

    def add(self, uid: int) -> None:
        self.add_user(User(uid))
        self.add_group(Group(uid))

    def delete(self, uid: int) -> None:
        self.delete_user(User(uid))
        self.delete_group(Group(uid))

    def is_user_and_group_exists(self, uid: int, gid: int = None) -> tuple[bool, bool]:
        is_user_exists = self.is_user_exists(uid)
        is_group_exists = self.is_group_exists(gid if gid else uid)

        return is_user_exists, is_group_exists
