from pprint import pprint
from ptrace.debugger import PtraceProcess, PtraceDebugger


class ProcessTracer:

    attached_processes: dict[str, PtraceProcess] = {}

    def __init__(self):
        self.debugger = PtraceDebugger()

    def attach(self, pid: int) -> PtraceProcess | None:
        try:

            if pid in self.attached_processes:
                print(f"[!] Process with PID {pid} is already being traced.")
                return self.attached_processes[pid]

            process = self.debugger.addProcess(pid, False)

            self._attach(process)
            # process.waitSignals()
            print(f"\t\\--> Attached to process [{pid}]")

            return process
        except Exception as e:
            print(f"[!] Failed to attach to PID {pid}: {e}")
            return None

    def kill(self, pid: int):
        try:
            print(f"[+] Attempting to kill process [{pid}]...")
            process = self.get_process(pid)

            print(f"\t\\--> Process found: {process}")
            if process is None:
                print(f"[!] No process found with PID {pid}.")
                self._detach(pid)
                return

            # IMPORTANT: To mute SIGNAL messages for the user permanently
            # we have to disable monitoring mode permanently
            # 'echo "export PROMPT_COMMAND='set +m'" >> /home/user/.bashrc && source /home/user/.bashrc'
            # In other words this will suppress "Terminated" being printed on the log

            print(f"[+] Detaching process [{pid}]...")
            self._detach(pid)
            # process.kill(signal.SIGTERM)
            print(f"\t\\--> Killed process [{pid}]!")
        except Exception as e:
            print(f"[!] Failed to kill process {pid}: {e}")
            return None

    def get_process(self, pid: int) -> PtraceProcess | None:
        return self.attached_processes.get(str(pid))

    def _attach(self, process: PtraceProcess):
        self.attached_processes[process.pid] = process
        pprint(self.attached_processes.get(process.pid))

    def _detach(self, pid: int):
        process = self.get_process(str(pid))

        if process is None:
            return

        self.resume_process(pid)
        process.detach()

    def resume_process(self, pid: int):
        process = self.get_process(pid)
        if process is None:
            return

        process.cont()
