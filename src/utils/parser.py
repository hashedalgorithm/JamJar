import shlex
from typing import List, Optional, Literal, Set, Tuple
import os

ParsedArgumentType = Literal["flag", "option", "positional", "special"]


class ParsedArgument:
    def __init__(
        self,
        type: ParsedArgumentType,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.type = type
        self.name = name
        self.value = value

    def __repr__(self):
        return f"ParsedArgument(type={self.type!r}, name={self.name!r}, value={self.value!r})"


class ParsedCommand:
    def __init__(self, command: str, args: List[ParsedArgument]):
        self.command = command
        self.args = args

    def __repr__(self):
        return f"ParsedCommand(command={self.command!r}, args={self.args!r})"

    def check_arg_exists(self, arg: str) -> bool:
        for parsed_arg in self.args:
            if parsed_arg.name == arg:
                return True
        return False

    def has_only_valid_args(
        self, valid_flags: Set[str], valid_options: Set[str]
    ) -> bool:
        for arg in self.args:
            if arg.type == "flag" and arg.name not in valid_flags:
                return False
            elif arg.type == "option" and arg.name not in valid_options:
                return False
            elif arg.type not in {"flag", "option", "positional", "special"}:
                return False
        return True

    def has_conflicting_options(self, conflict_pairs: List[Tuple[str, str]]) -> bool:
        seen = set(arg.name for arg in self.args if arg.type in {"flag", "option"})
        for a, b in conflict_pairs:
            if a in seen and b in seen:
                return True
        return False

    def group(self, type: list[ParsedArgumentType], values: set[str]):
        group: list[ParsedArgument] = []
        for arg in self.args:
            if arg.type in type:
                if "positional" != arg.type:
                    group.append(arg)
                    continue

                if arg.name in values:
                    group.append(arg)
        return group


class CommandParser:
    def __init__(self, options_with_values: Optional[List[str]] = None):
        self.options_with_values = options_with_values or []

    def set_options_with_values(self, options: List[str]) -> None:
        self.options_with_values = options

    def parse(self, command_line: str) -> ParsedCommand:
        tokens = shlex.split(command_line.strip())
        if not tokens:
            return ParsedCommand(command="", args=[])

        command = tokens[0]
        raw_args = tokens[1:]
        parsed_args = self._parse_args(raw_args)
        return ParsedCommand(command=command, args=parsed_args)

    def _parse_args(self, args: List[str]) -> List[ParsedArgument]:
        parsed: List[ParsedArgument] = []
        parsing_options = True
        i = 0

        while i < len(args):
            arg = args[i]

            if parsing_options and arg == "--":
                parsing_options = False
                i += 1
                continue

            if arg == "-":
                parsed.append(ParsedArgument(type="special", value="-"))
                i += 1
                continue

            if parsing_options and arg.startswith("-") and arg != "-":
                if "=" in arg:
                    opt, val = arg.split("=", 1)
                    parsed.append(ParsedArgument(type="option", name=opt, value=val))
                    i += 1
                    continue

                if len(arg) > 2 and not arg.startswith("--"):
                    for ch in arg[1:]:
                        flag = f"-{ch}"
                        parsed.append(ParsedArgument(type="flag", name=flag))
                    i += 1
                    continue

                if arg in self.options_with_values:
                    if i + 1 < len(args):
                        parsed.append(
                            ParsedArgument(type="option", name=arg, value=args[i + 1])
                        )
                        i += 2
                        continue
                    else:
                        parsed.append(
                            ParsedArgument(type="option", name=arg, value=None)
                        )
                        i += 1
                        continue

                parsed.append(ParsedArgument(type="flag", name=arg))
                i += 1
                continue

            parsed.append(ParsedArgument(type="positional", value=arg))
            i += 1

        return parsed

    def split_path(self, path: str) -> list[str]:
        if not path:
            return []

        tokens = path.split("/")
        stack = []

        is_absolute = path.startswith("/")

        for token in tokens:
            if token == "" or token == ".":
                continue
            elif token == "..":
                if stack and stack[-1] not in ["/", "."]:
                    stack.pop()
                elif not stack and is_absolute:
                    continue
                else:
                    stack.append("..")
            else:
                stack.append(token)
        if is_absolute:
            return ["/"] + stack
        elif path.startswith("."):
            return ["."] + stack
        else:
            return stack
