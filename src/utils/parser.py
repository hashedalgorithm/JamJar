import shlex
import re
from typing import Optional


class Command:
    def __init__(
        self,
        command: str,
        args: Optional[list[str]] = None,
        stdin: Optional[str] = None,
        stdout: Optional[str] = None,
        stdout_append: Optional[str] = None,
    ):
        self.command: str = command
        self.args: list[str] = args
        self.stdin: str = stdin
        self.stdout: str = stdout
        self.stdout_append: str = stdout_append

    def __repr__(self):
        return f"Command(command={self.command!r}, args={self.args!r}, stdin={self.stdin!r}, stdout={self.stdout!r}, stdout_append={self.stdout_append!r})"


class CommandSequence:
    def __init__(self, pipeline: list[Command], next_op: Optional[str] = None):
        self.pipeline: list[Command] = pipeline
        self.next_op: Optional[str] = next_op  # "&&", "||", ";", "&", or None

    def __repr__(self):
        return f"CommandSequence(pipeline={self.pipeline!r}, next_op={self.next_op!r})"


class ParserOption:
    def __init__(
        self,
        type: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.type: str = type  # "flag", "option", "positional", "special"
        self.name: str = name
        self.value: str = value

    def __repr__(self):
        return f"ParsedOption(name={self.name!r}, type={self.type!r}, value={self.value!r})"


class Parser:
    def __init__(self, command_line_str: str):
        self.command_line_str: str = command_line_str
        self.parsed = self.parse_shell_command(command_line_str)
        self.command_sequence: list[CommandSequence] = []

    def path_to_list_helper(path: str) -> list:
        return path.strip("/").split("/") if path != "/" and path != "" else []

    def split_by_operators(self, command_line: str):
        pattern = r"(;|&&|\|\||&)"
        parts = re.split(f"({pattern})", command_line)

        result: list[tuple[str, str]] = []
        buffer: str = ""

        for part in parts:
            part = part.strip()
            if part in {";", "&&", "||", "&"}:
                if buffer:
                    result.append((buffer.strip(), part))
                    buffer = ""
            else:
                if buffer:
                    buffer += " " + part
                else:
                    buffer = part

        if buffer:
            result.append((buffer.strip(), None))

        return result

    def parse_redirection(self, tokens: str) -> tuple[list[str], Command]:
        result: list[str] = []
        redir: Command = {}

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == ">":
                # Always overwrite previous stdout or stdout_append on seeing new >
                redir.pop("stdout_append", None)  # remove append if any
                redir["stdout"] = tokens[i + 1]
                i += 2
            elif token == ">>":
                # Always overwrite previous stdout or stdout_append on seeing new >>
                redir.pop("stdout", None)  # remove overwrite if any
                redir["stdout_append"] = tokens[i + 1]
                i += 2
            elif token == "<":
                # Only one stdin expected, overwrite if multiple (optional)
                redir["stdin"] = tokens[i + 1]
                i += 2
            else:
                result.append(token)
                i += 1

        return result, redir

    def preprocess_multiline_command(self, command_line: str) -> str:
        # Remove backslash-newline (line continuation) and replace with space
        return command_line.replace("\\\n", " ")

    def parse_shell_command(self, raw_input: str) -> list:
        command_line: str = raw_input.replace("\\\n", " ")
        command_groups: list[CommandSequence] = []
        segments = self.split_by_operators(command_line)

        for segment, operator_after in segments:
            pipeline_parts = segment.split("|")
            pipeline: list[Command] = []

            for part in pipeline_parts:
                part = part.strip()
                if not part:
                    continue

                try:
                    tokens = shlex.split(part)
                except ValueError as e:
                    raise ValueError(f"Failed to parse command: '{part}' - {e}")

                if tokens:
                    cleaned_tokens, redirection = self.parse_redirection(tokens)
                    cmd = {"command": cleaned_tokens[0], "args": cleaned_tokens[1:]}
                    cmd.update(redirection)
                    pipeline.append(cmd)

            if pipeline:
                command_groups.append({"pipeline": pipeline, "next_op": operator_after})

        return command_groups


class ArgumentParser:

    def __init__(self, args: list[str], opts_with_values: list[str] | None = None):
        self.parsed: list[ParserOption] = self.parse_arguments_structured(
            args, opts_with_values
        )

    def __repr__(self):
        return f"ArgumentParser(parsed={self.parsed!r})"

    def parse_arguments_structured(
        self, arguments: list[str], options_with_values=None
    ):
        if options_with_values is None:
            options_with_values = []

        parsed_args: list[ParserOption] = []
        parsing_options = True
        i = 0
        while i < len(arguments):
            arg = arguments[i]

            if parsing_options and arg == "--":
                parsed_args.append({"type": "special", "value": "--"})
                parsing_options = False
                i += 1
                continue

            if arg == "-":
                parsed_args.append({"type": "special", "value": "-"})
                i += 1
                continue

            if parsing_options and arg.startswith("-") and arg != "-":
                if "=" in arg:
                    opt, val = arg.split("=", 1)
                    parsed_args.append({"type": "option", "name": opt, "value": val})
                    i += 1
                    continue

                if arg in options_with_values:
                    if i + 1 < len(arguments):
                        parsed_args.append(
                            {"type": "option", "name": arg, "value": arguments[i + 1]}
                        )
                        i += 2
                        continue
                    else:
                        parsed_args.append(
                            {"type": "option", "name": arg, "value": None}
                        )
                        i += 1
                        continue
                else:
                    parsed_args.append({"type": "flag", "name": arg})
                    i += 1
                    continue

            parsed_args.append({"type": "positional", "value": arg})
            i += 1

        return parsed_args


# # --- Example Usage ---
# if __name__ == "__main__":
#     test_inputs = [
#         "ls",
#         "cp file1.txt file2.txt",
#         "ls -la /home/user",
#         "grep --ignore-case pattern file.txt",
#         'echo "Hello World"',
#         "mkdir My\\ Folder",
#         "echo 'Hello    World'",
#         "echo 'Hello' > output.txt",
#         "ps aux | grep python",
#         "VAR=value ./script.sh",
#         "sleep 5 &",
#         'echo "This is a test" >> result\\ file.txt',
#         "echo $(date)",
#         "cat < input.txt > output.txt >> log.txt",
#         "cat < input.txt \\\n| grep hello \\\n> output.txt >> final.log",
#     ]

#     for input_cmd in test_inputs:
#         print(input_cmd)

#         parser = Parser(input_cmd)
#         # result = parse_shell_command(input_cmd)
#         print(parser.parsed)

#     args = [
#         "-a",
#         "-o",
#         "output.txt",
#         "--verbose",
#         "--file=log.txt",
#         "input1.txt",
#         "--",
#         "-notAnOption",
#     ]
#     opts_with_values = ["-o", "--file"]

#     argparser = ArgumentParser(args, opts_with_values)
#     # parsed = argparse_arguments_structured(args, opts_with_values)

#     import pprint

#     pprint.pprint(argparser)
