
// This version uses security_bprm_check to trace execve calls and filter by
// UID.

#include <linux/binfmts.h>
#include <linux/fs.h>
#include <linux/sched.h>
#include <linux/types.h>
// #include <uapi/linux/ptrace.h>

#define TASK_COMM_LEN 128

struct trigger_data {
  int pid;
};

BPF_PERF_OUTPUT(syscall_trigger_events);

static int trigger_event_perf_submit(struct pt_regs *ctx,
                                     struct trigger_data *data) {
  syscall_trigger_events.perf_submit(ctx, data, sizeof(*data));
  return 1;
}

int trace_creds_for_exec(struct pt_regs *ctx, struct linux_binprm *bprm) {
  struct trigger_data trigger_data = {};

  trigger_data.pid = bpf_get_current_pid_tgid() >> 32;

  bpf_trace_printk("Exec syscall entry for PID: %d\\n", trigger_data.pid);

  trigger_event_perf_submit(ctx, &trigger_data);
  return 0;
}