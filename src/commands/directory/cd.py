from utils.parser import ParsedCommand
from commands.base import CommandBase
from models.file_system import FileSystem, Directory


class CD(CommandBase):
    def __init__(self, file_system: FileSystem, parsed: ParsedCommand) -> None:
        super().__init__("cd")
        self.file_system = file_system
        self.parsed = parsed
        
    def run(self) -> str | None:
        valid_flags = {"-@", "-L", "-P", "-e", "--help"}

        # Validate flags/options presence
        if not self.parsed.has_only_valid_args(valid_flags, set()):
            invalid_flags = [
                arg.name for arg in self.parsed.args if arg.type == "flag" and arg.name not in valid_flags
            ]
            return (
                f"bash: cd: {invalid_flags[0]}: invalid option\n"
                "cd: usage: cd [-L|[-P [-e]] [-@]] [dir]"
            )

        flags = [arg.name for arg in self.parsed.args if arg.type == "flag"]
        positional_args = [arg.value for arg in self.parsed.args if arg.type == "positional"]

        # Too many positional args error
        if len(positional_args) > 1:
            return "bash: cd: too many arguments"

        # Handle --help flag early
        if "--help" in flags:
            return """cd: cd [-L|[-P [-e]] [-@]] [dir]
Change the shell working directory.

Change the current directory to DIR.  The default DIR is the value of the
HOME shell variable. If DIR is "-", it is converted to $OLDPWD.

The variable CDPATH defines the search path for the directory containing
DIR.  Alternative directory names in CDPATH are separated by a colon (:).
A null directory name is the same as the current directory.  If DIR begins
with a slash (/), then CDPATH is not used.

If the directory is not found, and the shell option `cdable_vars' is set,
the word is assumed to be a variable name.  If that variable has a value,
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
-P is used; non-zero otherwise."""

        # -@ is invalid option according to your snippet
        if "-@" in flags:
            return (
                "bash: cd: -@: invalid option\n"
                "cd: usage: cd [-L|[-P [-e]] [-@]] [dir]"
            )

        # Determine mode, last occurrence wins, default to -L
        mode = "L"
        for f in flags:
            if f == "-L":
                mode = "L"
            elif f == "-P":
                mode = "P"

        # Default directory is home (~) if no positional arg
        input_path = positional_args[0] if positional_args else "~"

        # Handle special token "-" (OLDPWD)
        for arg in self.parsed.args:
            if arg.type == "special" and arg.value == "-":
                if hasattr(self.file_system, "oldpwd") and self.file_system.oldpwd:
                    # swap cwd and oldpwd
                    self.file_system.cwd, self.file_system.oldpwd = (
                        self.file_system.oldpwd,
                        self.file_system.cwd,
                    )
                    self.file_system.path_stack, self.file_system.oldpwd_path_stack = (
                        self.file_system.oldpwd_path_stack,
                        self.file_system.path_stack,
                    )
                    return None
                else:
                    return "bash: cd: OLDPWD not set"

        # Split input path into components
        path_components = self.parser.split_path(input_path)

        # Determine starting directory and initial path stack based on first component
        if path_components[0] == "~":
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

        # Traverse path components
        for comp in path_components:
            if comp == "..":
                if current_dir != self.file_system.root:
                    current_dir = current_dir.parent
                    current_path_stack.pop()
            else:
                if comp in current_dir.children and isinstance(current_dir.children[comp], Directory):
                    current_dir = current_dir.children[comp]
                    current_path_stack.append(comp)
                else:
                    # Compose full path string for error message
                    full_path = (
                        "/" + "/".join(current_path_stack[1:] + [comp])
                        if current_path_stack[0] == "root"
                        else "/".join(current_path_stack + [comp])
                    )
                    return f"bash: cd: {full_path}: No such file or directory"

        # Update oldpwd and cwd on success
        self.file_system.oldpwd = self.file_system.cwd
        self.file_system.oldpwd_path_stack = self.file_system.path_stack.copy()

        self.file_system.cwd = current_dir
        self.file_system.path_stack = current_path_stack

        return None
