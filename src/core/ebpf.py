from typing import Any
from bcc import BPF
from utils.helper import get_username_by_uid
from core.process_tracer import ProcessTracer, Process
from core.subroutines import Subroutines
from utils.logger import Logger


class EBPF(Logger):

    def __init__(self, ebpf_path: str):
        super().__init__()
        self.process_tracer = ProcessTracer()
        self.bpf = BPF(text=self.load_bpf_c_code(ebpf_path))
        self.subroutines = Subroutines(self.process_tracer)
        self.perf_buffer_name = "syscall_trigger_events"

        # Hooking into Security BRPM Creds for Exec
        self.bpf.attach_kprobe(
            event="security_bprm_creds_for_exec", fn_name="trace_creds_for_exec"
        )

    def load_bpf_c_code(self, ebpf_path: str) -> str:
        try:
            with open(ebpf_path, "r") as f:
                bpf_source = f.read()
                return bpf_source
        except FileNotFoundError:
            self.logger.fatal(f"Could not find eBPF source file at {ebpf_path}.")
            exit(1)

    def intialize_hook_points(self):
        self.bpf[self.perf_buffer_name].open_perf_buffer(self.syscall_trigger_callback)

    def get_perf_buffer_events(self, data: Any) -> list[Any]:
        return self.bpf[self.perf_buffer_name].event(data)

    def syscall_trigger_callback(self, cpu: int, data: Any, size: int) -> None:
        event = self.get_perf_buffer_events(data)

        if event.pid in self.process_tracer.attached_processes:
            self.logger.warning(f"Process already been paused -  {event.pid}.")
            return

        process = self.process_tracer.attach(event.pid)
        self.handle_attached_process(process)

    def handle_attached_process(self, process: Process):

        username = get_username_by_uid(process.uid)

        self.subroutines.subroutine_manager(
            process,
            username,
        )
