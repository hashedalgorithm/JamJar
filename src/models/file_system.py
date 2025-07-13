from __future__ import annotations
from models.directory import Directory
from models.file import File
from utils.helper import get_username_by_uid


class ParsedPath:
    def __init__(self, path: str):
        self.path: list[str] = (
            path.split("/") if not path.startswith("/") else path.strip("/").split("/")
        )
        self.is_absolute: bool = path.startswith("/")

    def __repr__(self):
        return f"ParsedPath(path={self.path}, isAbsolute={self.is_absolute})"


class FileSystem:
    def __init__(self, uid: int = 1000) -> None:
        self.root: Directory = Directory(name="root", parent="/")
        self.create_fake_dir_data_helper()

        self.cwd: Directory = self.get_default_cwd(uid)  # Current working directory
        self.path_stack: str[list] = ["root"]

        self.oldpwd = None  # Previous working directory (Directory object)
        self.oldpwd_path_stack = None  # Previous path stack (list of strings)

    def get_default_cwd(self, uid: int = 1000) -> Directory | None:
        username = get_username_by_uid(uid)

        home = self.root.children.get("home")
        if home is None:
            raise KeyError("Home directory does not exist in the file system.")
        user_dir = home.children.get(username)
        if user_dir is None:
            raise KeyError(f"User directory '{username}' does not exist in /home.")
        return user_dir

    def create_fake_dir_data_helper(self) -> None:
        # Setup fake FS environment (similar to your original)
        self.root.add(Directory("home", perm="drwxr-xr-x"))
        self.root.add(Directory("bin", perm="drwxr-xr-x"))
        self.root.add(Directory("sbin", perm="drwxr-xr-x"))
        self.root.add(Directory("lib", perm="drwxr-xr-x"))
        self.root.add(Directory("etc", perm="drwxr-xr-x"))
        self.root.add(Directory("var", perm="drwxr-xr-x"))
        self.root.add(Directory("tmp", perm="drwxrwxrwx"))
        self.root.add(Directory("usr", perm="drwxr-xr-x"))
        self.root.add(Directory("dev", perm="drwxr-xr-x"))

        home = self.root.children["home"]
        username = get_username_by_uid() or "user"

        home.add(Directory(username, perm="drwxr-xr-x"))

        user = home.children[username]

        user.add(Directory(".bash_history", perm="-rw------"))
        user.add(Directory(".bashrc", perm="-rw-r--r--"))
        user.add(Directory(".cache", perm="drwx------"))
        user.add(Directory("Desktop", perm="drwxr-xr-x"))
        user.add(Directory("Documents", perm="drwxr-xr-x"))
        user.add(Directory("Downloads", perm="drwxr-xr-x"))
        user.add(Directory("Music", perm="drwxr-xr-x"))
        user.add(Directory("Pictures", perm="drwxr-xr-x"))
        user.add(Directory("Puvlic", perm="drwxr-xr-x"))
        user.add(Directory("Templates", perm="drwxr-xr-x"))
        user.add(Directory("Videos", perm="drwxr-xr-x"))
        user.add(Directory(".ssh", perm="drwx------"))
        user.add(Directory(".profile", perm="-rw-r--r--"))
        user.add(Directory("a", perm="drw-r--rwx"))
        user.add(Directory("b", perm="drw-r--rwx"))

        a_folder = user.children["a"]

        # Add files to 'a'
        user.add(
            File(
                "abc.txt",
                perm="-rwx-w--wx",
            )
        )
        user.add(
            File(
                "test_file.txt",
                perm="-r--r--r--",
            )
        )
        user.add(
            File(
                "test1.txt",
                perm="-rw-rw-rw-",
            )
        )
        user.add(
            File(
                "test2.txt",
                perm="-rw-r--rw-",
            )
        )
        user.add(
            File(
                "notes.txt",
                perm="-rw-r--r--",
            )
        )
        user.add(
            File(
                "data.csv",
                perm="-rw-r--r--",
            )
        )
        user.add(
            File(
                "protected.txt",
                perm="-r--r--r--",
            )
        )
        user.add(
            Directory(
                "d",
                perm="drw-r--r-x",
            )
        )
        user.add(
            Directory(
                "emptydir",
                perm="drwxr-xr-x",
            )
        )

        b_folder = user.children["b"]
        b_folder.add(Directory("c", perm="drw-r--r--"))

        mydir = Directory("mydir", perm="drwxr-xr-x")
        mydir.add(File("file_in_mydir.txt", perm="-rw-r--r--"))
        user.add(mydir)

        myfolder = Directory("myfolder", perm="drwxr-xr-x")
        myfolder.add(File("file1.txt", perm="-rw-r--r--"))
        myfolder.add(File("file2.txt", perm="-rw-r--r--"))
        user.add(myfolder)

        dirA = Directory("dirA", perm="drwxr-xr-x")
        dirA.add(File("a1.txt", perm="-rw-r--r--"))
        dirA.add(File("a2.txt", perm="-rw-r--r--"))
        user.add(dirA)

        dirB = Directory("dirB", perm="drwxr-xr-x")
        dirB.add(File("b1.txt", perm="-rw-r--r--"))
        subB = Directory("subB", perm="drwxr-xr-x")
        subB.add(File("b2.txt", perm="-rw-r--r--"))
        dirB.add(subB)
        user.add(dirB)

    def check_directory_exists(self, path: str) -> bool:
        directory = self.get_directory(path)

        if directory is None:
            raise ValueError(f"No file/directory exists")

        return directory

    def get_directory(self, path: str) -> Directory:
        parsed_path = ParsedPath(path if path.__len__() > 0 else self.cwd.get_path())

        target_dir = self.root if parsed_path.is_absolute else self.cwd

        if target_dir is None:
            raise ValueError(f"No root/cwd found!")

        for _path in parsed_path.path:
            target_dir = target_dir.find_entry(_path)

        if target_dir is None:
            raise ValueError(f"No file/directory exists as {parsed_path.path[-1]}")

        return target_dir
