
// This version uses security_bprm_check to trace execve calls and filter by UID.

#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/fs.h>

#define ARGSIZE  128
#define UID_FILTER 1000 // Change this to the UID you want to filter

// PID as in the userspace term (i.e. task->tgid in kernel)
// Parent PID as in the userspace term (i.e task->real_parent->tgid in kernel)
struct event_data_t {
    u32 pid;  
    u32 ppid;
    u32 uid;
    char comm[TASK_COMM_LEN];
    char argv[ARGSIZE];
};

// BPF_PERF_OUTPUT(events);
BBF_PERF_OUTPUT(events);
BBF_PERF_OUTPUT(syscall_return_events);

static int entry_perf_submit(struct pt_regs *ctx, struct entry_event_data_t *data) {
    syscall_entry_events.perf_submit(ctx, data, sizeof(*data));
    return 0;
}

int security_bprm_check(struct linux_binprm *bprm) {
    struct entry_event_data_t data = {};
    struct task_struct *task;

    data.pid = bpf_get_current_pid_tgid() >> 32;

    task = (struct task_struct *)bpf_get_current_task();
    data.ppid = task->real_parent->tgid;


    int comm_ret = bpf_get_current_comm(&data.comm, sizeof(data.comm));
    if(comm_ret < 0) {
        bpf_trace_printk("Failed to get current comm, ret: %d\\n", comm_ret);
        return 0;
    }

    int ret = bpf_probe_read_user_str(args_concat, sizeof(args_concat), filename);
    if (ret < 0) {
        bpf_trace_printk("Failed to read filename, ret: %d\\n", ret);
        return 0;
    }

    #pragma unroll
    for (int i = 1; i < 20; i++) {     
        // const char *argp = NULL;

        int pt_ret = bpf_probe_read_user(&argp, sizeof(argp), &bprm->argv[i]);


        if (pt_ret < 0 || !argp) {
            bpf_trace_printk("Failed to read argument %d, ret: %d\\n", i, ret);
            break; // Stop if we hit a NULL pointer
        }

        // if (offset >= sizeof(args_concat) - 1) {
        //     break; // Prevent buffer overflow
        // }

        ret = bpf_probe_read_user_str(, sizeof(argp), argp);
        if (ret < 0) {
            bpf_trace_printk("Failed to read argument %d, ret: %d\\n", i, ret);
            break;
        }

        // // offset += ret; // Exclude the null terminator for concatenation
        // if (offset < sizeof(args_concat) - 1) {
        //     args_concat[offset++] = ' '; // Add a space between arguments
        // }


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