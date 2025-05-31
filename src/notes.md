libcurl4--openssl-dev
liblaujit-5.1-dev

to add vmlinux.h
This command extracts the BTF information from the kernel and generates the vmlinux.h file.
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

To check if the vmlinux file exists, run the following command in your terminal:

If the file exists, it will list the file. If it does not exist, you will see an error like ls: cannot access '/sys/kernel/btf/vmlinux': No such file or directory.

