import datetime
from typing import Dict, Optional, List, Tuple, Union

# === Base Class ===
class Document:
    def __init__(self, name: str, perm: str, xxx: str, owner: str, group: str, size: str, created_month: str, created_day: str, created_time: str) -> None:
        self.perm = perm
        self.xxx = xxx
        self.owner = owner
        self.group = group
        self.size = size
        self.created_month = created_month
        self.created_day = created_day
        self.created_time = created_time
        self.name = name

# === File ===
class File(Document):
    def __init__(self, name: str, perm: str = "drwxrwxrwx", xxx: str = "1",
                 owner: str = "root", group: str = "root", size: str = "4096",
                 created_month: str = datetime.datetime.now().strftime("%b"),
                 created_day: str = datetime.datetime.now().strftime("%d"),
                 created_time: str = datetime.datetime.now().strftime("%H:%M"),
                 content: str = "") -> None:
        super().__init__(name, perm, xxx, owner, group, size, created_month, created_day, created_time)
        self.content = content

    def write(self, content: str) -> None:
        self.content = content

    def append(self, content: str) -> None:
        self.content += content

    def read(self) -> str:
        return self.content

# === Folder ===
class Folder(Document):
    def __init__(self, name: str, perm: str = "drwxrwxrwx", xxx: str = "1",
                 owner: str = "root", group: str = "root", size: str = "4096",
                 created_month: str = datetime.datetime.now().strftime("%b"),
                 created_day: str = datetime.datetime.now().strftime("%d"),
                 created_time: str = datetime.datetime.now().strftime("%H:%M")) -> None:
        super().__init__(name, perm, xxx, owner, group, size, created_month, created_day, created_time)
        self.children: Dict[str, Document] = {}

    def add(self, doc: Document) -> None:
        if doc.name in self.children:
            raise ValueError(f"'{doc.name}' already exists in '{self.name}'.")
        self.children[doc.name] = doc

    def delete_something(self, names: List[str]) -> None:
        for n in names:
            del self.children[n]

    def clear(self) -> None:
        self.children = {}

# === Symbolic Link ===
class Symlink(Document):
    def __init__(self, name: str, target: str, perm: str = "lrwxrwxrwx", xxx: str = "1",
                 owner: str = "root", group: str = "root", size: str = "4096",
                 created_month: str = datetime.datetime.now().strftime("%b"),
                 created_day: str = datetime.datetime.now().strftime("%d"),
                 created_time: str = datetime.datetime.now().strftime("%H:%M")) -> None:
        super().__init__(name, perm, xxx, owner, group, size, created_month, created_day, created_time)
        self.target = target  # The name of the file/folder it points to

# === File System ===
class FileSystem:
    def __init__(self) -> None:
        self.root: Folder = Folder("root")
        self.cwd: Folder = self.root
        self.path_stack: List[Folder] = []

# === Helper Functions ===
def resolve_path(root: Folder, path: str) -> Tuple[Optional[Folder], Optional[str]]:
    """
    Resolves a path string to its parent Folder and the final component name.
    Returns (parent_folder, final_name) or (None, None) if not found.
    """
    if not path or path == ".":
        return (root, ".")
    parts = path.strip("/").split("/")
    curr = root
    for part in parts[:-1]:
        if part in curr.children and isinstance(curr.children[part], Folder):
            curr = curr.children[part]
        else:
            return (None, None)
    return (curr, parts[-1])

def has_write_permission(folder: Folder) -> bool:
    """
    Checks if the folder has write permission for the owner.
    """
    # Permission string: drwxrwxrwx
    # Check the third character (owner write)
    return len(folder.perm) > 2 and folder.perm[2] == "w"

# === Fake Directory Tree ===
def create_fake_dir_data_helper() -> FileSystem:
    FS = FileSystem()
    # Top-level folders
    FS.root.add(Folder('home', perm='drwxr-xr-x'))
    FS.root.add(Folder('bin', perm='drwxr-xr-x'))
    FS.root.add(Folder('sbin', perm='drwxr-xr-x'))
    FS.root.add(Folder('lib', perm='drwxr-xr-x'))
    FS.root.add(Folder('etc', perm='drwxr-xr-x'))
    FS.root.add(Folder('var', perm='drwxr-xr-x'))
    FS.root.add(Folder('tmp', perm='drwxrwxrwx'))
    FS.root.add(Folder('usr', perm='drwxr-xr-x'))
    FS.root.add(Folder('dev', perm='drwxr-xr-x'))
    # User folders and files
    FS.root.children['home'].add(Folder('strawberry', perm='drwxr-xr-x'))
    FS.root.children['home'].children['strawberry'].add(Folder('a', perm='drw-r--rwx'))
    a = FS.root.children['home'].children['strawberry'].children['a']
    a.add(File('.bash_history', perm='-rw-------'))
    a.add(File('abc.txt', perm='-rwx-w--wx'))
    a.add(File('test_file.txt', perm='-r--r--r--'))
    a.add(File('test1.txt', perm='-rw-rw-rw-'))
    a.add(File('test2.txt', perm='-rw-r--rw-'))
    a.add(File('notes.txt', perm='-rw-r--r--'))
    a.add(File('data.csv', perm='-rw-r--r--'))
    a.add(File('protected.txt', perm='-r--r--r--'))
    a.add(Folder('b', perm='drw-r--r-x'))
    a.add(Folder('d', perm='drw-r--r-x'))
    a.children['b'].add(Folder('c', perm='drw-r--r--'))
    a.add(Folder('emptydir', perm='drwxr-xr-x'))
    # Directory with a file inside
    mydir = Folder('mydir', perm='drwxr-xr-x')
    mydir.add(File('file_in_mydir.txt', perm='-rw-r--r--'))
    a.add(mydir)
    # Directory with multiple files
    myfolder = Folder('myfolder', perm='drwxr-xr-x')
    myfolder.add(File('file1.txt', perm='-rw-r--r--'))
    myfolder.add(File('file2.txt', perm='-rw-r--r--'))
    a.add(myfolder)
    # More directories with files and subfolders
    dirA = Folder('dirA', perm='drwxr-xr-x')
    dirA.add(File('a1.txt', perm='-rw-r--r--'))
    dirA.add(File('a2.txt', perm='-rw-r--r--'))
    a.add(dirA)
    dirB = Folder('dirB', perm='drwxr-xr-x')
    dirB.add(File('b1.txt', perm='-rw-r--r--'))
    subB = Folder('subB', perm='drwxr-xr-x')
    subB.add(File('b2.txt', perm='-rw-r--r--'))
    dirB.add(subB)
    a.add(dirB)
    # Symbolic link
    a.add(Symlink('link_to_test1.txt', 'test1.txt'))
    # Directory with no write permission
    nowrite = Folder('nowrite', perm='dr-xr-xr-x')
    nowrite.add(File('file_in_nowrite.txt', perm='-rw-r--r--'))
    a.add(nowrite)
    return FS

fs: FileSystem = create_fake_dir_data_helper()

# === RM Command ===
def rm(args: List[str]) -> Optional[str]:
    """
    Simulated rm command. Handles files, directories, symlinks, permissions, and flags.
    """
    cwd = fs.root.children['home'].children['strawberry'].children['a']
    flags = [arg for arg in args if arg.startswith('-')]
    files = [arg for arg in args if not arg.startswith('-')]

    # Handle --version and --help
    if '--version' in args:
        return (
            "rm (GNU coreutils) 9.4\n"
            "Copyright (C) 2023 Free Software Foundation, Inc.\n"
            "License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.\n"
            "This is free software: you are free to change and redistribute it.\n"
            "There is NO WARRANTY, to the extent permitted by law.\n\n"
            "Written by Paul Rubin, David MacKenzie, Richard M. Stallman,\n"
            "and Jim Meyering.\n"
        )
    if '--help' in args:
        return (
            "Usage: rm [OPTION]... [FILE]...\n"
            "Remove (unlink) the FILE(s).\n\n"
            "  -f, --force           ignore nonexistent files and arguments, never prompt\n"
            "  -I                    prompt once before removing more than three files, or\n"
            "                          when removing recursively; less intrusive than -i,\n"
            "                          while still giving protection against most mistakes\n"
            "      --interactive[=WHEN]  prompt according to WHEN: never, once (-I), or\n"
            "                          always (-i); without WHEN, prompt always\n"
            "      --one-file-system  when removing a hierarchy recursively, skip any\n"
            "                          directory that is on a file system different from\n"
            "                          that of the corresponding command line argument\n"
            "      --no-preserve-root  do not treat '/' specially\n"
            "      --preserve-root[=all]  do not remove '/' (default);\n"
            "                              with 'all', reject any command line argument\n"
            "                              on a separate device from its parent\n"
            "  -r, -R, --recursive   remove directories and their contents recursively\n"
            "  -d, --dir             remove empty directories\n"
            "  -v, --verbose         explain what is being done\n"
            "      --help        display this help and exit\n"
            "      --version     output version information and exit\n\n"
            "By default, rm does not remove directories.  Use the --recursive (-r or -R)\n"
            "option to remove each listed directory, too, along with all of its contents.\n\n"
            "To remove a file whose name starts with a '-', for example '-foo',\n"
            "use one of these commands:\n"
            "  rm -- -foo\n"
            "  rm ./-foo\n\n"
            "Note that if you use rm to remove a file, it might be possible to recover\n"
            "some of its contents, given sufficient expertise and/or time.  For greater\n"
            "assurance that the contents are truly unrecoverable, consider using shred(1).\n\n"
            "GNU coreutils online help: <https://www.gnu.org/software/coreutils/>\n"
            "Full documentation <https://www.gnu.org/software/coreutils/rm>\n"
            "or available locally via: info '(coreutils) rm invocation'\n"
        )

    recursive = any('r' in flag for flag in flags)
    force = any('f' in flag for flag in flags)
    verbose = any('v' in flag for flag in flags)
    dir_only = any('d' in flag for flag in flags)

    outputs: List[str] = []

    for name in files:
        # Special cases for . and ..
        if name in ('.', '..'):
            outputs.append(f"rm: cannot remove '{name}': Is a directory")
            continue

        # Handle nested paths (e.g., nowrite/file_in_nowrite.txt)
        parent, base = resolve_path(cwd, name)
        if parent is None or base is None or base not in parent.children:
            if not force:
                outputs.append(f"rm: cannot remove '{name}': No such file or directory")
            continue

        # Permission check for parent directory
        if not has_write_permission(parent):
            outputs.append(f"rm: cannot remove '{name}': Permission denied")
            continue

        target = parent.children[base]

        if isinstance(target, Folder):
            if dir_only:
                if target.children:
                    outputs.append(f"rm: cannot remove '{name}': Directory not empty")
                    continue
                del parent.children[base]
                if verbose:
                    outputs.append(f"removed directory: '{name}'")
            elif recursive:
                del parent.children[base]
                if verbose:
                    outputs.append(f"removed directory: '{name}'")
            else:
                outputs.append(f"rm: cannot remove '{name}': Is a directory")
        elif isinstance(target, Symlink):
            del parent.children[base]
            if verbose:
                outputs.append(f"removed symbolic link '{name}'")
        else:
            if dir_only:
                outputs.append(f"rm: cannot remove '{name}': Not a directory")
                continue
            del parent.children[base]
            if verbose:
                outputs.append(f"removed '{name}'")

    return "\n".join(outputs) if outputs else None

# === Test Cases ===
testing_commands: List[List[str]] = [
    ['.bash_history', 'abc.txt'],
    ['-f', 'test_file.txt'],
    ['-v', '-r', 'b'],
    ['-d', 'd'],
    ['-rf', '/'],
    ['-d', 'test2.txt'],
    ['b'],
    ['-d', 'b'],
    ['-d', 'mydir'],
    ['not_a_file.txt'],
    ['-f', 'not_a_file.txt'],
    ['-r', 'myfolder'],
    ['--version'],
    ['--help'],
    ['-rf', 'dirA'],
    ['-rv', 'dirB'],
    ['link_to_test1.txt'],
    ['test1.txt', 'not_a_file.txt', 'abc.txt', 'missing.txt'],
    ['nowrite/file_in_nowrite.txt'],
    ['.'],
    ['..'],
]

# === Test Runner ===
if __name__ == "__main__":
    for args in testing_commands:
        print(f"rm {' '.join(args)}:")
        output = rm(args)
        print(output)
        print('-' * 40)