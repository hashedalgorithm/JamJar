// two bpf ring buffer events for syscall entry

#include <linux/fs.h>
#include <linux/sched.h>
#include <uapi/linux/ptrace.h>

#define ARGSIZE 128
#define MAX_ARG_LIMIT 50 // Maximum number of arguments to read
#define UID_FILTER 1000  // Change this to the UID you want to filter

// pid -> PID as in the userspace term (i.e. task->tgid in kernel)
// ppid -> Parent PID as in the userspace term (i.e task->real_parent->tgid in
// kernel)
struct trigger_data {
  u32 pid;
};

struct event_data {
  u32 pid;
  u32 ppid;
  u32 uid;
  char comm[TASK_COMM_LEN];
  char args[ARGSIZE];
  int retval;
};

struct temp_args_holder {
  char args[ARGSIZE];
};

BPF_ARRAY(args_map, struct temp_args_holder, 1);
BPF_ARRAY(event_map, struct event_data, 1);

BPF_PERF_OUTPUT(syscall_trigger_events);
BPF_PERF_OUTPUT(syscall_events);

static int trigger_event_perf_submit(struct pt_regs *ctx,
                                     struct trigger_data *data) {
  syscall_trigger_events.perf_submit(ctx, data, sizeof(*data));
  return 1;
}

static int event_perf_submit(struct pt_regs *ctx, struct event_data *data) {
  syscall_events.perf_submit(ctx, data, sizeof(*data));
  return 1;
}

int handle_exec_syscall_entry(struct pt_regs *ctx, const char __user *filename,
                              const char __user *const __user *__argv,
                              const char __user *const __user *__envp) {

  struct trigger_data trigger_data = {};

  trigger_data.pid = bpf_get_current_pid_tgid() >> 32;

  // Submitting the entry event so that process can be attached to debugger
  trigger_event_perf_submit(ctx, &trigger_data);

  u32 event_map_index = 0;
  struct task_struct *task;
  struct event_data *event_data = event_map.lookup(&event_map_index);
  if (!event_data) {
    bpf_trace_printk("Failed to get event_data from event_map\\n");
    return 0;
  }
  event_data->pid = trigger_data.pid;
  event_data->uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
  task = (struct task_struct *)bpf_get_current_task();
  event_data->ppid = task->real_parent->tgid;

  int ret = bpf_get_current_comm(&event_data->comm, sizeof(event_data->comm));
  if (ret < 0) {
    bpf_trace_printk("Failed to read current command, ret: %d\\n", ret);
    return 0;
  }

  if (ret > ARGSIZE) {
    bpf_trace_printk("Command length exceeds ARGSIZE exiting\\n");
    return 0;
  }

  int offset = ret;
  u32 args_map_index = 0;
  struct temp_args_holder *temp_args_holder_ptr =
      args_map.lookup(&args_map_index);

  if (!temp_args_holder_ptr) {
    bpf_trace_printk("Failed to get args buffer from map\\n");
    return 0;
  }

  char *temp_args_buffer = temp_args_holder_ptr->args;

  if (!temp_args_holder_ptr) {
    bpf_trace_printk("Failed to get args_ptr from args_map\\n");
    return 0;
  }

  temp_args_buffer = temp_args_buffer + offset;
  int args_processing_ret = 0;

#pragma unroll
  for (int i = 1; i < MAX_ARG_LIMIT; i++) {
    const char *argp = NULL;

    int ret = bpf_probe_read_user(&argp, sizeof(argp), &__argv[i]);
    if (ret < 0 || !argp) {
      bpf_trace_printk("Failed to read pointer %d, ret: %d\\n", i, ret);
      break;
    }

    ret = bpf_probe_read_user_str(&temp_args_buffer, sizeof(argp), &argp);

    int remaining_space = ARGSIZE - offset;
    int used_space = offset + ret;

    if (ret < 0) {
      bpf_trace_printk("Failed to read argument %d, ret: %d\\n", i, ret);
      args_processing_ret = -1;
      break;
    }

    if (ret < remaining_space) {
      temp_args_buffer = temp_args_buffer + ret;
    }

    offset += ret;
  }

  if (ret < 0) {
    bpf_trace_printk("Failed to process(concat) arguments from user space\\n");
    return 0;
  }

  bpf_trace_printk("Concatenated args: %s\\n", &event_data->args);

  event_perf_submit(ctx, event_data);

  return 0;
}

// int handle_exec_syscall_return(struct pt_regs *ctx) {
//   struct event_data data = {};
//   struct task_struct *task;

//   u32 uid = bpf_get_current_uid_gid() & 0xffffffff;
//   if (uid != UID_FILTER) {
//     return 0;
//   }

//   data.pid = bpf_get_current_pid_tgid() >> 32;
//   data.uid = uid;

//   task = (struct task_struct *)bpf_get_current_task();
//   data.ppid = task->real_parent->tgid;

//   // bpf_get_current_comm(&data.comm, sizeof(data.comm));
//   data.retval = PT_REGS_RC(ctx);
//   event_perf_submit(ctx, &data);
//   return 0;
// }