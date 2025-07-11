from __future__ import annotations
from .directory import Directory
from models.file import File
from utils.helper import get_username_by_uid


class FileSystem:
    def __init__(self) -> None:
        self.root = Directory("root")
        self.cwd = self.root  # Current working directory
        self.path_stack = ['root']

        self.oldpwd = None              # Previous working directory (Directory object)
        self.oldpwd_path_stack = None   # Previous path stack (list of strings)

        self.create_fake_dir_data_helper()

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
        a_folder = home.children[username]

        a_folder.add(Directory("a", perm="drw-r--rwx"))
        a_folder = a_folder.children["a"]

        # Add files to 'a'
        a_folder.add(File(".bash_history", perm="-rw-------"))
        a_folder.add(File("abc.txt", perm="-rwx-w--wx"))
        a_folder.add(File("test_file.txt", perm="-r--r--r--"))
        a_folder.add(File("test1.txt", perm="-rw-rw-rw-"))
        a_folder.add(File("test2.txt", perm="-rw-r--rw-"))
        a_folder.add(File("notes.txt", perm="-rw-r--r--"))
        a_folder.add(File("data.csv", perm="-rw-r--r--"))
        a_folder.add(File("protected.txt", perm="-r--r--r--"))
        a_folder.add(Directory("b", perm="drw-r--r-x"))
        a_folder.add(Directory("d", perm="drw-r--r-x"))
        a_folder.add(Directory("emptydir", perm="drwxr-xr-x"))

        b_folder = a_folder.children["b"]
        b_folder.add(Directory("c", perm="drw-r--r--"))

        mydir = Directory("mydir", perm="drwxr-xr-x")
        mydir.add(File("file_in_mydir.txt", perm="-rw-r--r--"))
        a_folder.add(mydir)

        myfolder = Directory("myfolder", perm="drwxr-xr-x")
        myfolder.add(File("file1.txt", perm="-rw-r--r--"))
        myfolder.add(File("file2.txt", perm="-rw-r--r--"))
        a_folder.add(myfolder)

        dirA = Directory("dirA", perm="drwxr-xr-x")
        dirA.add(File("a1.txt", perm="-rw-r--r--"))
        dirA.add(File("a2.txt", perm="-rw-r--r--"))
        a_folder.add(dirA)

        dirB = Directory("dirB", perm="drwxr-xr-x")
        dirB.add(File("b1.txt", perm="-rw-r--r--"))
        subB = Directory("subB", perm="drwxr-xr-x")
        subB.add(File("b2.txt", perm="-rw-r--r--"))
        dirB.add(subB)
        a_folder.add(dirB)