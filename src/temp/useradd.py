import crypt
import random
import string

class User:
    def __init__(self, username, uid, gid, full_name, home, shell, password_hash="!"):
        self.username = username
        self.uid = uid
        self.gid = gid
        self.full_name = full_name
        self.home = home
        self.shell = shell
        self.password_hash = password_hash

class Group:
    def __init__(self, name, gid):
        self.name = name
        self.gid = gid
        self.members = []

class FakeLinuxSystem:
    def __init__(self):
        self.users = {}
        self.groups = {}
        self.shadows = {}
        self.next_uid = 1000
        self.next_gid = 1000

        # Root user and group
        self.groups["root"] = Group("root", 0)
        self.users["root"] = User("root", 0, 0, "root", "/root", "/bin/bash", "!")
        self.shadows["root"] = "!"

    def group_exists(self, group_name):
        return group_name in self.groups

    def add_group(self, group_name):
        if self.group_exists(group_name):
            return self.groups[group_name].gid
        gid = self.next_gid
        self.next_gid += 1
        self.groups[group_name] = Group(group_name, gid)
        return gid

    def hash_password(self, password):
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return crypt.crypt(password, f"$6${salt}$")

    def add_user(self, username, full_name="", shell="/bin/bash", password=None, group_name=None):
        if username in self.users:
            return f"useradd: user '{username}' already exists"

        gid = self.add_group(group_name or username)
        uid = self.next_uid
        self.next_uid += 1
        home = f"/home/{username}"
        password_hash = self.hash_password(password) if password else "!"

        user = User(username, uid, gid, full_name, home, shell, password_hash)
        self.users[username] = user
        self.shadows[username] = password_hash
        self.groups[group_name or username].members.append(username)

        return f"user '{username}' created with UID {uid}, GID {gid}, home '{home}', shell '{shell}'"

    def get_passwd(self):
        lines = []
        for u in self.users.values():
            lines.append(f"{u.username}:x:{u.uid}:{u.gid}:{u.full_name}:{u.home}:{u.shell}")
        return "\n".join(lines)

    def get_shadow(self):
        lines = []
        for u in self.users.values():
            lines.append(f"{u.username}:{self.shadows[u.username]}:19000:0:99999:7:::")
        return "\n".join(lines)

    def get_group(self):
        lines = []
        for g in self.groups.values():
            members_str = ",".join(g.members)
            lines.append(f"{g.name}:x:{g.gid}:{members_str}")
        return "\n".join(lines)

# Useradd command imitation
def useradd(system, args):
    import argparse
    parser = argparse.ArgumentParser(prog="useradd", add_help=False)
    parser.add_argument("username")
    parser.add_argument("-c", dest="comment", default="")
    parser.add_argument("-s", dest="shell", default="/bin/bash")
    parser.add_argument("-p", dest="password", default=None)
    parser.add_argument("-g", dest="group", default=None)

    try:
        parsed = parser.parse_args(args)
    except Exception as e:
        return f"useradd: error: {e}"

    return system.add_user(
        parsed.username,
        full_name=parsed.comment,
        shell=parsed.shell,
        password=parsed.password,
        group_name=parsed.group
    )

# Test cases
if __name__ == "__main__":
    system = FakeLinuxSystem()

    tests = [
        ["alice", "-c", "Alice Doe", "-s", "/bin/zsh", "-p", "AlicePass123", "-g", "developers"],
        ["bob", "-c", "Bob Smith", "-p", "BobPass456"],
        ["charlie", "-s", "/bin/fish"],
        ["dave"]
    ]

    for test_args in tests:
        print(f"useradd {' '.join(test_args)}")
        output = useradd(system, test_args)
        print(output)
        print("-" * 50)

    print("\n=== /etc/passwd ===")
    print(system.get_passwd())

    print("\n=== /etc/shadow ===")
    print(system.get_shadow())

    print("\n=== /etc/group ===")
    print(system.get_group())
