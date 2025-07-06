from models.file_system import Directory, FileSystem
from utils.parser import CommandParser, ParsedCommand
from commands.base import CommandBase

class CD(CommandBase):
    def __init__(self, file_system: FileSystem) -> None:
        super().__init__()
        self.file_system = file_system
        self.parser = CommandParser()

    def run(self, parsed_command: ParsedCommand) -> str | None:
        # Define valid flags
        valid_flags = {"-@", "-L", "-P", "-e", "--help"}

        flags = []
        positional_args = []

        # Separate flags and positional args from parsed_command.args
        for arg in parsed_command.args:
            if arg.type == "flag":
                if arg.name not in valid_flags:
                    return (
                        f"bash: cd: {arg.name}: invalid option\n"
                        "cd: usage: cd [-L|[-P [-e]] [-@]] [dir]"
                    )
                flags.append(arg.name)
            elif arg.type == "positional":
                positional_args.append(arg.value)

        # Check too many positional arguments
        if len(positional_args) > 1:
            return "bash: cd: too many arguments"

        # Handle --help flag
        if "--help" in flags:
            return '''cd: cd [-L|[-P [-e]] [-@]] [dir]
Change the shell working directory.

Change the current directory to DIR.  The default DIR is the value of the
HOME shell variable. If DIR is "-", it is converted to $OLDPWD.

The variable CDPATH defines the search path for the directory containing
DIR.  Alternative directory names in CDPATH are separated by a colon (:).
A null directory name is the same as the current directory.  If DIR begins
with a slash (/), then CDPATH is not used.

If the directory is not found, and the shell option `cdable_vars' is set,
the word is assumed to be  a variable name.  If that variable has a value,
its value is used for DIR.

Options:
-L    force symbolic links to be followed: resolve symbolic
        links in DIR after processing instances of `..'
-P    use the physical directory structure without following
        symbolic links: resolve symbolic links in DIR before
        processing instances of `..'
-e    if the -P option is supplied, and the current working
        directory cannot be determined successfully, exit with
        a non-zero status
-@    on systems that support it, present a file with extended
        attributes as a directory containing the file attributes

The default is to follow symbolic links, as if `-L' were specified.
`..' is processed by removing the immediately previous pathname component
back to a slash or the beginning of DIR.

Exit Status:
Returns 0 if the directory is changed, and if $PWD is set successfully when
-P is used; non-zero otherwise.
'''

        # Handle -@ flag: invalid option per your snippet
        if "-@" in flags:
            return "bash: cd: -@: invalid option\ncd: usage: cd [-L|[-P [-e]] [-@]] [dir]"

        # Determine mode based on flags: last -L or -P wins, default to -L
        mode = "L"
        for f in flags:
            if f == "-L":
                mode = "L"
            elif f == "-P":
                mode = "P"

        # Default path to home/root if no positional arg
        if not positional_args:
            # Go home (root in your FS)
            self.file_system.oldpwd = self.file_system.cwd
            self.file_system.oldpwd_path_stack = self.file_system.path_stack.copy()

            self.file_system.cwd = self.file_system.root
            self.file_system.path_stack = ["root"]
            return None

        # Extract path arg (only one positional arg guaranteed here)
        input_path = positional_args[0]

        # Handle cd - (OLDPWD)
        if input_path == "-":
            if hasattr(self.file_system, "oldpwd") and self.file_system.oldpwd:
                self.file_system.cwd, self.file_system.oldpwd = self.file_system.oldpwd, self.file_system.cwd
                self.file_system.path_stack, self.file_system.oldpwd_path_stack = (
                    self.file_system.oldpwd_path_stack,
                    self.file_system.path_stack,
                )
                return None
            else:
                return "bash: cd: OLDPWD not set"

        # Use your parser's split_path function to tokenize and normalize the path
        path_components = self.parser.split_path(input_path)

        # Determine starting directory and path stack based on first component
        if path_components[0] == "~":
            # Expand ~ to /root/home/strawberry
            try:
                current_dir = self.file_system.root.children["home"].children["strawberry"]
            except KeyError:
                return "bash: cd: no such user directory for ~"
            current_path_stack = ["root", "home", "strawberry"]
            path_components = path_components[1:]
        elif path_components[0] == "/":
            current_dir = self.file_system.root
            current_path_stack = ["root"]
            path_components = path_components[1:]
        elif path_components[0] == ".":
            current_dir = self.file_system.cwd
            current_path_stack = self.file_system.path_stack.copy()
            path_components = path_components[1:]
        else:
            current_dir = self.file_system.cwd
            current_path_stack = self.file_system.path_stack.copy()

        # Process path components
        for comp in path_components:
            if comp == "..":
                if current_dir != self.file_system.root:
                    current_dir = current_dir.parent
                    current_path_stack.pop()
            else:
                # Check if comp exists and is a directory
                if comp in current_dir.children and isinstance(current_dir.children[comp], Directory):
                    current_dir = current_dir.children[comp]
                    current_path_stack.append(comp)
                else:
                    # Compose a path string for error
                    if current_path_stack[0] == "root":
                        full_path = "/" + "/".join(current_path_stack[1:] + [comp])
                    else:
                        full_path = "/".join(current_path_stack + [comp])
                    return f"bash: cd: {full_path}: No such file or directory"

        # Update OLDPWD and cwd on success
        self.file_system.oldpwd = self.file_system.cwd
        self.file_system.oldpwd_path_stack = self.file_system.path_stack.copy()

        self.file_system.cwd = current_dir
        self.file_system.path_stack = current_path_stack

        return None

if __name__ == "__main__":
    # Mock or minimal FileSystem and Directory setup for testing
    class Directory:
        def __init__(self, name):
            self.name = name
            self.children = {}
            self.parent = None

        def add_child(self, child):
            self.children[child.name] = child
            child.parent = self

        def __repr__(self):
            return f"Directory({self.name})"

    class FileSystem:
        def __init__(self):
            self.root = Directory("root")
            self.cwd = self.root
            self.path_stack = ["root"]
            self.oldpwd = None
            self.oldpwd_path_stack = []

    from utils.parser import CommandParser, ParsedCommand, ParsedArgument

    # Setup a fake FS tree: /root/home/strawberry and /root/etc
    fs = FileSystem()
    home = Directory("home")
    strawberry = Directory("strawberry")
    etc = Directory("etc")
    fs.root.add_child(home)
    home.add_child(strawberry)
    fs.root.add_child(etc)

    cd_command = CD(fs)

    # Helper to build ParsedCommand manually (simulate parsing)
    def build_parsed_command(command: str, args_list: list[str]) -> ParsedCommand:
        # Build ParsedArgument list with positional args only for simplicity
        args = [ParsedArgument(type="positional", value=a) for a in args_list]
        return ParsedCommand(command=command, args=args)

    # Test cases
    tests = [
        ("cd", []),
        ("cd", [".."]),
        ("cd", ["-"]),
        ("cd", ["~"]),
        ("cd", ["-L"]),
        ("cd", ["-P"]),
        ("cd", ["-Q"]),
        ("cd", ["~", "-L"]),
        ("cd", ["../../etc"]),
        ("cd", ["/etc"]),
        ("cd", ["nonexistent"]),
        ("cd", ["-L", "-P"]),
        ("cd", ["--help"]),
    ]

    for cmd_name, args_list in tests:
        parsed_cmd = build_parsed_command(cmd_name, args_list)
        result = cd_command.run(parsed_cmd)
        print(f"Command: {cmd_name} {' '.join(args_list)}")
        if result is not None:
            print(result)
        else:
            print(f"New cwd: {fs.cwd.name}, Path stack: {fs.path_stack}")
        print("-" * 40)
