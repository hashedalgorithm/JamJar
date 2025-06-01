import shlex
import re

def split_by_operators(command_line: str) -> list[tuple[str, str | None]]:
    pattern = r'(;|&&|\|\||&)'
    parts = re.split(f'({pattern})', command_line)

    result = []
    buffer = ''

    for part in parts:
        part = part.strip()
        if part in {';', '&&', '||', '&'}:
            if buffer:
                result.append((buffer.strip(), part))
                buffer = ''
        else:
            if buffer:
                buffer += ' ' + part
            else:
                buffer = part

    if buffer:
        result.append((buffer.strip(), None))

    return result

def parse_redirection(tokens: list[str]) -> tuple[list[str], dict[str, str]]:
    result = []
    redir = {}
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token == '>':
            redir.pop('stdout_append', None)
            redir['stdout'] = tokens[i + 1]
            i += 2
        elif token == '>>':
            redir.pop('stdout', None)
            redir['stdout_append'] = tokens[i + 1]
            i += 2
        elif token == '<':
            redir['stdin'] = tokens[i + 1]
            i += 2
        else:
            result.append(token)
            i += 1

    return result, redir

def preprocess_multiline_command(command_line: str) -> str:
    return command_line.replace('\\\n', ' ')

def parse_shell_command(raw_input: str) -> list[dict[str, object]]:
    command_line = preprocess_multiline_command(raw_input)
    command_groups = []
    segments = split_by_operators(command_line)

    for segment, operator_after in segments:
        pipeline_parts = segment.split('|')
        pipeline = []

        for part in pipeline_parts:
            part = part.strip()
            if not part:
                continue

            try:
                tokens = shlex.split(part)
            except ValueError as e:
                raise ValueError(f"Failed to parse command: '{part}' - {e}")

            if tokens:
                cleaned_tokens, redirection = parse_redirection(tokens)
                cmd = {
                    "command": cleaned_tokens[0],
                    "args": cleaned_tokens[1:]
                }
                cmd.update(redirection)
                pipeline.append(cmd)

        if pipeline:
            command_groups.append({
                "pipeline": pipeline,
                "next_op": operator_after
            })

    return command_groups

def parse_arguments_structured(arguments: list[str], options_with_values: list[str] = None) -> list[dict[str, str | None]]:
    if options_with_values is None:
        options_with_values = []

    parsed_args = []
    parsing_options = True
    i = 0

    while i < len(arguments):
        arg = arguments[i]

        if parsing_options and arg == '--':
            parsed_args.append({'type': 'special', 'value': '--'})
            parsing_options = False
            i += 1
            continue

        if arg == '-':
            parsed_args.append({'type': 'special', 'value': '-'})
            i += 1
            continue

        if parsing_options and arg.startswith('-') and arg != '-':
            if '=' in arg:
                opt, val = arg.split('=', 1)
                parsed_args.append({'type': 'option', 'name': opt, 'value': val})
                i += 1
                continue

            if arg in options_with_values:
                if i + 1 < len(arguments):
                    parsed_args.append({'type': 'option', 'name': arg, 'value': arguments[i + 1]})
                    i += 2
                    continue
                else:
                    parsed_args.append({'type': 'option', 'name': arg, 'value': None})
                    i += 1
                    continue
            else:
                parsed_args.append({'type': 'flag', 'name': arg})
                i += 1
                continue

        parsed_args.append({'type': 'positional', 'value': arg})
        i += 1

    return parsed_args


# --- Example Usage ---
if __name__ == "__main__":
    test_inputs = [
        "ls",
        "cp file1.txt file2.txt",
        "ls -la /home/user",
        "grep --ignore-case pattern file.txt",
        'echo "Hello World"',
        "mkdir My\\ Folder",
        "echo 'Hello    World'",
        "echo 'Hello' > output.txt",
        "ps aux | grep python",
        "VAR=value ./script.sh",
        "sleep 5 &",
        'echo "This is a test" >> result\\ file.txt',
        "echo $(date)",
        "cat < input.txt > output.txt >> log.txt",
        "cat < input.txt \\\n| grep hello \\\n> output.txt >> final.log"
    ]

    for input_cmd in test_inputs:
        print(f"\nInput: {input_cmd}")
        parsed = parse_shell_command(input_cmd)
        print(parsed)

    args = ['-a', '-o', 'output.txt', '--verbose', '--file=log.txt', 'input1.txt', '--', '-notAnOption']
    opts_with_values = ['-o', '--file']
    parsed_args = parse_arguments_structured(args, opts_with_values)

    import pprint
    pprint.pprint(parsed_args)
