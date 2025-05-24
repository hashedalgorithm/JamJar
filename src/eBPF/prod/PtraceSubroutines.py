from ptrace.debugger import PtraceProcess
import signal
import cmd_invoke
import time

# Object for cmd API
CMD = cmd_invoke.CMD_invoke()


# ------------------------------- Helper Functions -----------------------------------------------------#
def write_to_proc(message: str, pid: int) -> None:
    if message != None:
        # Set path for the process to write to
        fd_path = f"/proc/{pid}/fd/1"
        try:
            # Open file descriptor for writing
            with open(fd_path, "w") as fd:
                fd.write(message)
        except Exception as e:
            print(f"Error: {e}")


def check_linebreak(message: str) -> str:
    if not message == None and not message.endswith("\n") and not message == "":
        return message + "\n"
    return message


# IMPORTANT: To mute SIGNAL messages for the user permanently we have to disable monitoring mode permanently 'echo "export PROMPT_COMMAND='set +m'" >> /home/user/.bashrc && source /home/user/.bashrc'
def kill_and_quit(process: PtraceProcess, pid: int) -> None:
    # Kill the process using SIGTERM
    process.kill(signal.SIGTERM)
    print(f"\t\\--> Attached to process [{pid}] and killed it!")


# ------------------------------- Directory Function handling ------------------------------------------#
def dir_routine(
    pid: int, ppid: int, command: str, cwd: str, running_process: PtraceProcess
) -> None:
    cmd_output = check_linebreak(CMD.invoke_dir(command, src_dir=cwd))

    # Write modified output to target process
    write_to_proc(cmd_output, str(ppid))
    kill_and_quit(running_process, str(pid))


# ------------------------------- Network Function handling --------------------------------------------#
def network_routine(pid: int, ppid: int, command: str, running_process: str) -> None:
    cmd_output = CMD.invoke_network(command)
    # Special case ping
    if type(cmd_output) == list:
        for n, item in enumerate(cmd_output):
            write_to_proc(item + "\n", str(ppid))
            if n < 5:
                time.sleep(1)
    # Write modified output to target process
    else:
        write_to_proc(check_linebreak(cmd_output), str(pid))
    kill_and_quit(running_process, str(pid))


# ------------------------------- Process Function handling --------------------------------------------#
def process_routine(
    pid: int,
    ppid: int,
    command: str,
    tty: str,
    uname: str,
    running_process: PtraceProcess,
) -> None:
    cmd_output = check_linebreak(CMD.invoke_process(command, tty, uname))
    # Write modified output to target process
    write_to_proc(cmd_output, str(ppid))
    kill_and_quit(running_process, str(pid))
