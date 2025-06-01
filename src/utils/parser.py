import shlex
import re

def split_by_operators(command_line):
    pattern = r'(;|&&|\|\||&)'
    parts = re.split(f'({pattern})', command_line)
    
    result = []
    buffer = ''
    operator = None

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

def parse_redirection(tokens):
    result = []
    redir = {}

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '>':
            # Always overwrite previous stdout or stdout_append on seeing new >
            redir.pop('stdout_append', None)  # remove append if any
            redir["stdout"] = tokens[i + 1]
            i += 2
        elif token == '>>':
            # Always overwrite previous stdout or stdout_append on seeing new >>
            redir.pop('stdout', None)  # remove overwrite if any
            redir["stdout_append"] = tokens[i + 1]
            i += 2
        elif token == '<':
            # Only one stdin expected, overwrite if multiple (optional)
            redir["stdin"] = tokens[i + 1]
            i += 2
        else:
            result.append(token)
            i += 1

    return result, redir

def preprocess_multiline_command(command_line):
    # Remove backslash-newline (line continuation) and replace with space
    return command_line.replace('\\\n', ' ')

def parse_shell_command(raw_input):
    command_line = raw_input.replace('\\\n', ' ')
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



def parse_arguments_structured(arguments, options_with_values=None):
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
                    parsed_args.append({'type': 'option', 'name': arg, 'value': arguments[i+1]})
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
        "echo $(date)" ,
        "cat < input.txt > output.txt >> log.txt",
        "cat < input.txt \\\n| grep hello \\\n> output.txt >> final.log" 
    ]

    for input_cmd in test_inputs:
        print(input_cmd)

        result = parse_shell_command(input_cmd)
        print(result)
    

    args = ['-a', '-o', 'output.txt', '--verbose', '--file=log.txt', 'input1.txt', '--', '-notAnOption']
    opts_with_values = ['-o', '--file']
    parsed = parse_arguments_structured(args, opts_with_values)

    import pprint
    pprint.pprint(parsed)
