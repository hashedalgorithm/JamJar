from typing import List, Optional, Union, Dict, Tuple

import datetime

# === File System Classes and Helpers (from rm.py) ===

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

class File(Document):
    def __init__(self, name: str, perm: str = "drwxrwxrwx", xxx: str = "1",
                 owner: str = "root", group: str = "root", size: str = "4096",
                 created_month: str = datetime.datetime.now().strftime("%b"),
                 created_day: str = datetime.datetime.now().strftime("%d"),
                 created_time: str = datetime.datetime.now().strftime("%H:%M"),
                 content: str = "") -> None:
        super().__init__(name, perm, xxx, owner, group, size, created_month, created_day, created_time)
        self.content = content

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

class Symlink(Document):
    def __init__(self, name: str, target: str, perm: str = "lrwxrwxrwx", xxx: str = "1",
                 owner: str = "root", group: str = "root", size: str = "4096",
                 created_month: str = datetime.datetime.now().strftime("%b"),
                 created_day: str = datetime.datetime.now().strftime("%d"),
                 created_time: str = datetime.datetime.now().strftime("%H:%M")) -> None:
        super().__init__(name, perm, xxx, owner, group, size, created_month, created_day, created_time)
        self.target = target

class FileSystem:
    def __init__(self) -> None:
        self.root: Folder = Folder("root")
        self.cwd: Folder = self.root
        self.path_stack: List[Folder] = []

def resolve_path(root: Folder, path: str) -> Tuple[Optional[Folder], Optional[str]]:
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

def create_fake_dir_data_helper() -> FileSystem:
    FS = FileSystem()
    FS.root.add(Folder('home', perm='drwxr-xr-x'))
    FS.root.add(Folder('bin', perm='drwxr-xr-x'))
    FS.root.add(Folder('sbin', perm='drwxr-xr-x'))
    FS.root.add(Folder('lib', perm='drwxr-xr-x'))
    FS.root.add(Folder('etc', perm='drwxr-xr-x'))
    FS.root.add(Folder('var', perm='drwxr-xr-x'))
    FS.root.add(Folder('tmp', perm='drwxrwxrwx'))
    FS.root.add(Folder('usr', perm='drwxr-xr-x'))
    FS.root.add(Folder('dev', perm='drwxr-xr-x'))
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
    mydir = Folder('mydir', perm='drwxr-xr-x')
    mydir.add(File('file_in_mydir.txt', perm='-rw-r--r--'))
    a.add(mydir)
    myfolder = Folder('myfolder', perm='drwxr-xr-x')
    myfolder.add(File('file1.txt', perm='-rw-r--r--'))
    myfolder.add(File('file2.txt', perm='-rw-r--r--'))
    a.add(myfolder)
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
    a.add(Symlink('link_to_test1.txt', 'test1.txt'))
    nowrite = Folder('nowrite', perm='dr-xr-xr-x')
    nowrite.add(File('file_in_nowrite.txt', perm='-rw-r--r--'))
    a.add(nowrite)
    return FS

fs: FileSystem = create_fake_dir_data_helper()

# === LS Command Implementation ===

def ls(args: List[str]) -> Optional[str]:
    cwd = fs.root.children['home'].children['strawberry'].children['a']
    flags = [arg for arg in args if arg.startswith('-')]
    paths = [arg for arg in args if not arg.startswith('-')]

    if '--version' in args:
        return (
            "ls (GNU coreutils) 9.4\n"
            "Copyright (C) 2023 Free Software Foundation, Inc.\n"
            "License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.\n"
            "Written by Richard Stallman and David MacKenzie.\n"
        )

    if '--help' in args:
        return (
            "Usage: ls [OPTION]... [FILE]...\n"
            "List information about the FILEs (the current directory by default).\n"
            "Options:\n"
            "  -a, --all             do not ignore entries starting with .\n"
            "  -d, --directory       list directories themselves, not their contents\n"
            "  -l                    use a long listing format\n"
            "  -R, --recursive       list subdirectories recursively\n"
            "  -h, --human-readable  with -l, print sizes in human readable format (e.g., 1K 234M 2G)\n"
            "      --help     display this help and exit\n"
            "      --version  output version information and exit\n"
        )

    show_all = '-a' in flags or '--all' in args
    long_format = '-l' in flags
    recursive = '-R' in flags or '--recursive' in args
    human = '-h' in flags or '--human-readable' in args
    dir_only = '-d' in flags or '--directory' in args

    targets = paths if paths else ['.']
    output_lines: List[str] = []

    def human_readable(size: Union[int, str]) -> str:
        try:
            size = int(size)
        except Exception:
            return str(size)
        for unit in ['B', 'K', 'M', 'G']:
            if size < 1024:
                return f"{size}{unit}"
            size = size // 1024
        return f"{size}G"

    def list_directory(folder: Folder, path_label: str = None) -> List[str]:
        lines = []
        entries = folder.children.items()
        if not show_all:
            entries = [(k, v) for k, v in entries if not k.startswith('.')]
        if path_label:
            lines.append(f"{path_label}:")
        for name, item in sorted(entries, key=lambda x: x[0]):
            if long_format:
                size = human_readable(item.size) if human else item.size
                line = f"{item.perm} {item.xxx} {item.owner} {item.group} {size} {item.created_month} {item.created_day} {item.created_time} {name}"
            else:
                line = name
            lines.append(line)
        return lines

    def handle_target(path: str) -> List[str]:
        parent, base = resolve_path(cwd, path)
        if path == '.':
            return list_directory(cwd)
        if parent and base in parent.children:
            item = parent.children[base]
            if isinstance(item, Folder):
                if dir_only:
                    return [base] if not long_format else [f"{item.perm} {item.xxx} {item.owner} {item.group} {item.size} {item.created_month} {item.created_day} {item.created_time} {item.name}"]
                lines = list_directory(item, path if len(targets) > 1 else None)
                if recursive:
                    for child in item.children.values():
                        if isinstance(child, Folder):
                            lines += [''] + handle_target(f"{path.rstrip('/')}/{child.name}")
                return lines
            else:
                return [base] if not long_format else [f"{item.perm} {item.xxx} {item.owner} {item.group} {item.size} {item.created_month} {item.created_day} {item.created_time} {item.name}"]
        else:
            return [f"ls: cannot access '{path}': No such file or directory"]

    for target in targets:
        output_lines += handle_target(target)
        if len(targets) > 1:
            output_lines.append("")  # Separate outputs for multiple targets

    return "\n".join(output_lines)

# === Extensive LS Test Cases ===

if __name__ == "__main__":
    test_ls_cmds = [
        [],  # default
        ['-l'],
        ['-a'],
        ['-la'],
        ['-lh'],
        ['-R'],
        ['-lR'],
        ['-alR'],
        ['-lhR'],
        ['-d', 'dirA'],
        ['dirA'],
        ['dirB'],
        ['mydir'],
        ['myfolder'],
        ['emptydir'],
        ['nowrite'],
        ['b'],
        ['b/c'],
        ['d'],
        ['test1.txt'],
        ['.bash_history'],
        ['link_to_test1.txt'],
        ['not_a_file.txt'],
        ['-l', 'test1.txt'],
        ['-l', 'link_to_test1.txt'],
        ['-l', 'not_a_file.txt'],
        ['--help'],
        ['--version'],
        ['-l', 'dirA', 'dirB'],
        ['-l', 'myfolder', 'mydir'],
        ['-l', 'test1.txt', 'abc.txt', 'missing.txt'],
        ['-a', 'dirA'],
        ['-a', 'myfolder'],
        ['-a', 'emptydir'],
        ['-R', 'dirB'],
        ['-R', 'myfolder'],
        ['-R', 'b'],
        ['-R', 'emptydir'],
        ['-R', 'not_a_file.txt'],
        ['-lh', 'dirA'],
        ['-lh', 'myfolder'],
        ['-lh', 'emptydir'],
        ['-lh', 'not_a_file.txt'],
        ['-d', '.'],
        ['-d', 'not_a_file.txt'],
        ['-d', 'dirA'],
        ['-d', 'myfolder'],
        ['-d', 'emptydir'],
        ['-d', 'b'],
        ['-d', 'd'],
        ['-d', 'nowrite'],
        ['-d', 'link_to_test1.txt'],
        ['-d', 'not_a_file.txt'],
    ]

    for i, args in enumerate(test_ls_cmds):
        print(f"\n=== ls {' '.join(args) if args else '(default)'} ===")
        print(ls(args))
        print("-" * 40)
