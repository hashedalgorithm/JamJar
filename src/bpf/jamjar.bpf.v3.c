#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/fs.h>

#define ARGSIZE  128
#define UID_FILTER 1000 // Change this to the UID you want to filter


struct entry_event_data_t {
    u32 pid;  // PID as in the userspace term (i.e. task->tgid in kernel)
    u32 ppid; // Parent PID as in the userspace term (i.e task->real_parent->tgid in kernel)
    u32 uid;
};

struct return_event_data_t {
    u32 pid;  
    u32 ppid;
    u32 uid;
    char comm[TASK_COMM_LEN];
    char argv[ARGSIZE];
    int retval;
};

// BPF_PERF_OUTPUT(events);
BBF_PERF_OUTPUT(syscall_entry_events);
BBF_PERF_OUTPUT(syscall_return_events);

static int entry_perf_submit(struct pt_regs *ctx, struct entry_event_data_t *data) {
    syscall_entry_events.perf_submit(ctx, data, sizeof(*data));
    return 0;
}

int handle_exec_syscall_entry(struct pt_regs *ctx,
    const char __user *filename,
    const char __user *const __user *__argv,
    const char __user *const __user *__envp)
{
    // Filter by UID 
    // commented out for now, as it may not be needed and increases execution time
    // u32 uid = bpf_get_current_uid_gid() & 0xffffffff;
    // if (uid != UID_FILTER) {
    //     return 0;
    // }

    struct entry_event_data_t data = {};
    struct task_struct *task;

    data.pid = bpf_get_current_pid_tgid() >> 32;

    task = (struct task_struct *)bpf_get_current_task();
    data.ppid = task->real_parent->tgid;

    // Submitting the entry event so that process can be attached to debugger
    entry_perf_submit(ctx, &data);


    struct 


    bpf_trace_printk("Concatenated args: %s\\n", args_concat);
    events.perf_submit(ctx, &args_concat, sizeof(args_concat));

    return 0;
}

int do_ret_sys_execve(struct pt_regs *ctx)
{
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