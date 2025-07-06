import datetime


class Document:
    def __init__(
        self,
        name,
        perm,
        xxx,
        owner,
        group,
        size,
        created_month,
        created_day,
        created_time,
    ) -> None:
        self.perm = perm
        self.xxx = xxx
        self.owner = owner
        self.group = group
        self.size = size
        self.created_month = created_month
        self.created_day = created_day
        self.created_time = created_time
        self.name = name


class File(Document):
    def __init__(
        self,
        name,
        perm="drwxrwxrwx",
        xxx="1",
        owner="root",
        group="root",
        size="4096",
        created_month=datetime.datetime.now().strftime("%b"),
        created_day=datetime.datetime.now().strftime("%d"),
        created_time=datetime.datetime.now().strftime("%H:%M"),
        content="",
    ):
        super().__init__(
            name,
            perm,
            xxx,
            owner,
            group,
            size,
            created_month,
            created_day,
            created_time,
        )
        self.content = content

    def write(self, content):
        self.content = content

    def append(self, content):
        self.content += content

    def read(self):
        return self.content


class Folder(Document):
    def __init__(
        self,
        name,
        perm="drwxrwxrwx",
        xxx="1",
        owner="root",
        group="root",
        size="4096",
        created_month=datetime.datetime.now().strftime("%b"),
        created_day=datetime.datetime.now().strftime("%d"),
        created_time=datetime.datetime.now().strftime("%H:%M"),
    ):
        super().__init__(
            name,
            perm,
            xxx,
            owner,
            group,
            size,
            created_month,
            created_day,
            created_time,
        )
        self.children = {}

    def add(self, doc):
        if doc.name in self.children:
            raise ValueError(f"'{doc.name}' already exists in '{self.name}'.")
        self.children[doc.name] = doc

    def delete_something(self, name):
        for n in name:
            del self.children[n]

    def clear(self):
        self.children = {}


class FileSystem:
    def __init__(self):
        self.root = Folder("root")
        self.cwd = self.root
        self.path_stack = []


def create_fake_dir_data_helper():
    FS = FileSystem()
    FS.root.add(Folder("home", perm="drwxr-xr-x"))
    FS.root.add(Folder("bin", perm="drwxr-xr-x"))
    FS.root.add(Folder("sbin", perm="drwxr-xr-x"))
    FS.root.add(Folder("lib", perm="drwxr-xr-x"))
    FS.root.add(Folder("etc", perm="drwxr-xr-x"))
    FS.root.add(Folder("var", perm="drwxr-xr-x"))
    FS.root.add(Folder("tmp", perm="drwxrwxrwx"))
    FS.root.add(Folder("usr", perm="drwxr-xr-x"))
    FS.root.add(Folder("dev", perm="drwxr-xr-x"))
    FS.root.children["home"].add(Folder("strawberry", perm="drwxr-xr-x"))
    FS.root.children["home"].children["strawberry"].add(Folder("a", perm="drw-r--rwx"))
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File(".bash_history", perm="-rw-------")
    )
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File("abc.txt", perm="-rwx-w--wx")
    )
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File("test_file.txt", perm="-r--r--r--")
    )
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File("test1.txt", perm="-rw-rw-rw-")
    )
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File("test2.txt", perm="-rw-r--rw-")
    )
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File("notes.txt", perm="-rw-r--r--")
    )  # Added file
    FS.root.children["home"].children["strawberry"].children["a"].add(
        File("data.csv", perm="-rw-r--r--")
    )  # Added file
    FS.root.children["home"].children["strawberry"].children["a"].add(
        Folder("b", perm="drw-r--r-x")
    )
    FS.root.children["home"].children["strawberry"].children["a"].add(
        Folder("d", perm="drw-r--r-x")
    )
    FS.root.children["home"].children["strawberry"].children["a"].children["b"].add(
        Folder("c", perm="drw-r--r--")
    )

    return FS


fs = create_fake_dir_data_helper()


testing_commands = [
    [".bash_history", "abc.txt"],
    ["-f", "test_file.txt"],
    ["-v", "-r", "b"],
    ["-d", "d"],
    ["-rf", "/"],
    ["-d", "test2.txt"],  # Test: try to remove a file with -d
    ["b"],  # Test: try to remove directory 'b' without -r or -d
    ["not_a_file.txt"],  # Test: try to remove a file that doesn't exist
    ["-f", "not_a_file.txt"],  # Force delete nonexistent file (should print nothing)
    ["--version"],  # Test: print version info
    ["--help"],  # Test: print help info
]
for args in testing_commands:
    print(f"rm {' '.join(args)}:")
    output = rm(args)
    print(output)
    print("-" * 40)
