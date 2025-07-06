import datetime
import crypt
import random
import string

# --- User and Group Classes ---
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

# --- Fake Linux System ---
class FakeLinuxSystem:
    def __init__(self):
        self.users = {}  # username -> User
        self.groups = {}  # group name -> Group
        self.shadows = {}  # username -> password hash
        self.filesystem = {"home": {}}
        self.next_uid = 1001
        self.next_gid = 1001

        # Create root user and group
        self.groups["root"] = Group("root", 0)
        self.users["root"] = User("root", 0, 0, "root", "/root", "/bin/bash", "!")
        self.shadows["root"] = "!"

    def user_exists(self, username):
        return username in self.users

    def group_exists(self, group_name):
        return group_name in self.groups

    def create_home_dir(self, username):
        self.filesystem["home"][username] = {}
        return f"/home/{username}"

    def add_group(self, name):
        if self.group_exists(name):
            return self.groups[name].gid
        gid = self.next_gid
        self.next_gid += 1
        self.groups[name] = Group(name, gid)
        return gid

    def hash_password(self, password):
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return crypt.crypt(password, f"$6${salt}$")  # SHA-512

    def add_user(self, username, full_name="", shell="/bin/bash", password=None, group_name=None):
        if self.user_exists(username):
            return f"adduser: The user '{username}' already exists."

        gid = self.add_group(group_name or username)
        uid = self.next_uid
        self.next_uid += 1
        home = self.create_home_dir(username)
        password_hash = self.hash_password(password) if password else "!"

        user = User(username, uid, gid, full_name, home, shell, password_hash)
        self.users[username] = user
        self.shadows[username] = password_hash
        self.groups[group_name or username].members.append(username)

        return f"User '{username}' created with UID {uid}, GID {gid}, home '{home}', shell '{shell}'"

    def get_passwd(self):
        return "\n".join(
            f"{u.username}:x:{u.uid}:{u.gid}:{u.full_name}:{u.home}:{u.shell}"
            for u in self.users.values()
        )

    def get_shadow(self):
        return "\n".join(
            f"{u.username}:{self.shadows[u.username]}:19000:0:99999:7:::"
            for u in self.users.values()
        )

    def get_group(self):
        return "\n".join(
            f"{g.name}:x:{g.gid}:{','.join(g.members)}"
            for g in self.groups.values()
        )

# --- Global System Instance ---
system = FakeLinuxSystem()

# --- adduser Command ---
def adduser(args):
    if len(args) < 1:
        return "adduser: missing username"
    username = args[0]
    full_name = " ".join(args[1:]) if len(args) > 1 else ""
    password = "Password123"  # Default password
    return system.add_user(username, full_name=full_name, password=password)

# --- useradd Command ---
def useradd(args):
    import argparse
    parser = argparse.ArgumentParser(prog="useradd", add_help=False)
    parser.add_argument("username")
    parser.add_argument("-c", dest="comment", default="")
    parser.add_argument("-s", dest="shell", default="/bin/bash")
    parser.add_argument("-p", dest="password", default=None)
    parser.add_argument("-g", dest="group", default=None)

    try:
        parsed_args = parser.parse_args(args)
    except Exception as e:
        return f"useradd: error: {e}"

    return system.add_user(
        parsed_args.username,
        full_name=parsed_args.comment,
        shell=parsed_args.shell,
        password=parsed_args.password,
        group_name=parsed_args.group
    )

# --- passwd Command ---
def passwd(args):
    if len(args) > 1:
        return "passwd: too many arguments"

    username = args[0] if args else "root"

    if username not in system.users:
        return f"passwd: user '{username}' does not exist"

    user = system.users[username]

    # Simulated password check
    old_password = input("Current password: ")
    hashed_input = crypt.crypt(old_password, user.password_hash)

    if hashed_input != user.password_hash:
        return "passwd: Authentication token manipulation error\npasswd: password unchanged"

    new_password = input("New password: ")
    confirm_password = input("Retype new password: ")

    if new_password != confirm_password:
        return "passwd: passwords do not match"

    new_hash = system.hash_password(new_password)
    user.password_hash = new_hash
    system.shadows[username] = new_hash

    return "passwd: password updated successfully"

# --- Run Tests ---
commands = [
    ("adduser", ["johnsmith", "John", "Smith"]),
    ("adduser", ["bob"]),
    ("useradd", ["-c", "Jane Smith", "-s", "/bin/zsh", "-p", "JanePass123", "janesmith"]),
    ("useradd", ["-c", "Mike D", "-p", "mikeSecurePass", "-g", "devs", "mike"]),
]

print("=== User Creation Tests ===")
for cmd, args in commands:
    print(f"{cmd} {' '.join(args)}:")
    output = adduser(args) if cmd == "adduser" else useradd(args)
    print(output)
    print("-" * 40)

# --- Change Password Test ---
print("=== Change Password for johnsmith ===")
print(passwd(["johnsmith"]))
print("-" * 40)

# --- Show Simulated Files ---
print("=== /etc/passwd ===")
print(system.get_passwd())
print("\n=== /etc/shadow ===")
print(system.get_shadow())
print("\n=== /etc/group ===")
print(system.get_group())