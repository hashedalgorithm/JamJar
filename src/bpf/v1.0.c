// Returns concatenated arguments of execve syscall for a specific UID (1000).

#include <linux/fs.h>
#include <linux/sched.h>
#include <uapi/linux/ptrace.h>

#define ARGSIZE 128
#define UID_FILTER 1000

enum event_type {
  EVENT_ARG,
  EVENT_RET,
};

struct data_t {
  u32 pid;  // PID as in the userspace term (i.e. task->tgid in kernel)
  u32 ppid; // Parent PID as in the userspace term (i.e task->real_parent->tgid
            // in kernel)
  u32 uid;
  char comm[TASK_COMM_LEN];
  enum event_type type;
  char argv[ARGSIZE];
  int retval;
};

BPF_PERF_OUTPUT(events);

static int __submit_arg(struct pt_regs *ctx, void *ptr, struct data_t *data) {
  bpf_probe_read_user(data->argv, sizeof(data->argv), ptr);
  events.perf_submit(ctx, data, sizeof(struct data_t));
  return 1;
}

static int submit_arg(struct pt_regs *ctx, void *ptr, struct data_t *data) {
  const char *argp = NULL;
  bpf_probe_read_user(&argp, sizeof(argp), ptr);

  if (bpf_probe_read_user(&argp, sizeof(argp), ptr) < 0 || !argp) {
    bpf_trace_printk("argp is NULL or unreadable\\n");
    return 0;
  }

  int ret = bpf_probe_read_user_str(data->argv, sizeof(data->argv), argp);

  if (ret < 0) {
    bpf_trace_printk("Read failed, ret: %d\\n", ret);
    return 0;
  }

  // Now you can log it safely
  bpf_trace_printk("arg: %s\\n", data->argv);

  bpf_trace_printk("ptr: %lx, argp: %lx, \\n", (unsigned long)ptr,
                   (unsigned long)argp);
  return __submit_arg(ctx, (void *)(argp), data);
}

int syscall__execve(struct pt_regs *ctx, const char __user *filename,
                    const char __user *const __user *__argv,
                    const char __user *const __user *__envp) {
  u32 uid = bpf_get_current_uid_gid() & 0xffffffff;
  if (uid != UID_FILTER) {
    return 0;
  }

  // create data here and pass to submit_arg to save stack space (#555)
  struct data_t data = {};
  struct task_struct *task;

  data.pid = bpf_get_current_pid_tgid() >> 32;

  task = (struct task_struct *)bpf_get_current_task();
  data.ppid = task->real_parent->tgid;

  int comm_ret = bpf_get_current_comm(&data.comm, sizeof(data.comm));
  if (comm_ret < 0) {
    bpf_trace_printk("Failed to get current comm, ret: %d\\n", comm_ret);
    return 0;
  }
  data.type = EVENT_ARG;

  // __submit_arg(ctx, (void *)filename, &data);

  // Concatenate all arguments into a single string
  char args_concat[ARGSIZE] = {0};
  int offset = 0;

  // Add the filename as the first argument
  int ret = bpf_probe_read_user_str(args_concat, sizeof(args_concat), filename);
  if (ret < 0) {
    bpf_trace_printk("Failed to read filename, ret: %d\\n", ret);
    return 0;
  }
  offset += ret; // Exclude the null terminator for concatenation

// skip first arg, as we submitted filename
#pragma unroll
  for (int i = 1; i < 20; i++) {
    // if (submit_arg(ctx, (void *)&__argv[i], &data) == 0)
    //     break;  // stop if we hit a NULL pointer

    const char *argp = NULL;
    if (bpf_probe_read_user(&argp, sizeof(argp), &__argv[i]) < 0 || !argp) {
      break; // Stop if we hit a NULL pointer
    }

    if (offset >= sizeof(args_concat) - 1) {
      break; // Prevent buffer overflow
    }

    ret = bpf_probe_read_user_str(&args_concat[offset], sizeof(argp), argp);
    if (ret < 0) {
      bpf_trace_printk("Failed to read argument %d, ret: %d\\n", i, ret);
      break;
    }

    offset += ret; // Exclude the null terminator for concatenation
    if (offset < sizeof(args_concat) - 1) {
      args_concat[offset++] = ' '; // Add a space between arguments
    }
  }

  // // handle truncated argument list
  char ellipsis[] = "...";

  __submit_arg(ctx, (void *)ellipsis, &data);

  // Submit the concatenated arguments
  // bpf_probe_read_user(data.argv, sizeof(data.argv), args_concat);
  bpf_trace_printk("Concatenated args: %s\\n", args_concat);
  events.perf_submit(ctx, &args_concat, sizeof(args_concat));

  return 0;
}

int do_ret_sys_execve(struct pt_regs *ctx) {
  struct data_t data = {};
  struct task_struct *task;

  u32 uid = bpf_get_current_uid_gid() & 0xffffffff;
  if (uid != UID_FILTER) {
    return 0;
  }

  data.pid = bpf_get_current_pid_tgid() >> 32;
  data.uid = uid;

  task = (struct task_struct *)bpf_get_current_task();
  data.ppid = task->real_parent->tgid;

  bpf_get_current_comm(&data.comm, sizeof(data.comm));
  data.type = EVENT_RET;
  data.retval = PT_REGS_RC(ctx);
  events.perf_submit(ctx, &data, sizeof(data));
  return 0;
}