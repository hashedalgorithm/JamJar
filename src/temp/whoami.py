import argparse

# Simulated user session
current_user = "root"

# Fake whoami command with dummy non-interactive options
def whoami(args=None):
    parser = argparse.ArgumentParser(prog="whoami", add_help=False)
    parser.add_argument("--verbose", action="store_true", help="Show detailed user info (fake)")
    parser.add_argument("--uid", action="store_true", help="Show user ID (fake)")
    parser.add_argument("--help", action="store_true", help="Display help for whoami")
    parser.add_argument("--version", action="store_true", help="Display version info for whoami")

    try:
        parsed_args = parser.parse_args(args)
    except Exception as e:
        return f"whoami: error parsing arguments: {e}"

    if parsed_args.help:
        return (
            "Usage: whoami [OPTION]...\n"
            "Print the user name associated with the current effective user ID.\n"
            "Same as id -un.\n\n"
            "      --help        display this help and exit\n"
            "      --version     output version information and exit\n\n"
            "GNU coreutils online help: <https://www.gnu.org/software/coreutils/>\n"
            "Full documentation <https://www.gnu.org/software/coreutils/whoami>\n"
            "or available locally via: info '(coreutils) whoami invocation'"
        )
    if parsed_args.version:
        return "whoami (honeypot version) 1.0.0"

    if parsed_args.verbose:
        return f"Username: {current_user}\nHome: /home/{current_user}\nShell: /bin/bash"
    elif parsed_args.uid:
        return f"UID: 0"
    else:
        return current_user

# Test cases
test_cases = [
    [],
    ["--help"],
    ["--version"],
    ["--verbose"],
    ["--uid"]
]

print("=== whoami Command Tests ===")
for args in test_cases:
    print(f"$ whoami {' '.join(args)}")
    print(whoami(args))
    print("-" * 40)