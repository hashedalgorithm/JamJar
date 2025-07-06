
#include <linux/fs.h>
#include <linux/sched.h>
#include <uapi/linux/ptrace.h>

struct trigger_data {
  u32 pid;
};

BPF_PERF_OUTPUT(syscall_trigger_events);

TRACEPOINT_PROBE(sched, sched_process_fork) {
  char comm[TASK_COMM_LEN];
  bpf_get_current_comm(&comm, sizeof(comm));

  // Filter: Only trace forks from "bash"
  if (!(comm[0] == 'b' && comm[1] == 'a' && comm[2] == 's' && comm[3] == 'h')) {
    return 0;
  }

  bpf_trace_printk("sched_process_fork: comm=%s\\n", comm);

  struct trigger_data trigger_data = {};
  trigger_data.pid = args->child_pid;

  bpf_trace_printk("BASH Fork: parent=%d child=%d\\n", args->parent_pid,
                   trigger_data.pid);

  syscall_trigger_events.perf_submit(args, &trigger_data, sizeof(trigger_data));

  return 0;
}
