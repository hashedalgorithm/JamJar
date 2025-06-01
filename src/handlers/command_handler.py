from handlers.directory_handler import DirectoryHandler
from handlers.network_handler import NetworkHandler
from handlers.process_handler import ProcessHandler
from handlers.file_ops_handler import FileOpsHandler
from handlers.system_handler import SystemHandler
from models.file_system import FileSystem
import logging


class CommandHandler:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="jamjar.log",  # Geil haha
    )

    def __init__(self) -> None:
        self.file_system = FileSystem()
        self.directory_handler = DirectoryHandler(file_system=self.file_system)
        self.network_handler = NetworkHandler()
        self.process_handler = ProcessHandler()
        self.file_ops_handler = FileOpsHandler()
        self.system_handler = SystemHandler()

    def invoke_directory_handler(self, cmd: str, src_dir: str = ""):
        logging.info(cmd)
        return self.directory_handler.handle(cmd, src_dir)

    def invoke_network_handler(self, cmd):
        logging.info(cmd)
        return self.network_handler.handle(cmd)

    def invoke_process_handler(self, cmd, tty, pid):
        logging.info(cmd)
        return self.process_handler.handle(cmd, tty, pid)

    def invoke_file_ops_handler(self, cmd):
        logging.info(cmd)
        return self.file_ops_handler.handle(cmd)

    def invoke_system_handler(self, cmd):
        logging.info(cmd)
        return self.system_handler.handle(cmd)


# if __name__ == "__main__":
# cmd = CommandHandler()
# print("Testing---------------------------------")
# print(cmd.invoke_dir("ls"))
# print(cmd.invoke_dir("ls home"))
# print(cmd.invoke_dir("ls", src_dir="/home"))
# print(cmd.invoke_dir("ls user", src_dir="/home"))
# print(cmd.invoke_dir("ls test_file", src_dir="/home/user"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("ls -al user", src_dir="/home"))
# print(cmd.invoke_dir("ls /home/user", src_dir="/home"))
# print(cmd.invoke_dir("ls user/.local", src_dir="/home"))
# print(cmd.invoke_dir("ls -al"))
# print(cmd.invoke_dir("ls -al not_here"))

# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("rm test_file", src_dir="/home/user"))
# print(cmd.invoke_dir("rm .ssh", src_dir="/home/user"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("rm -rf .ssh", src_dir="/home/user"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("rm"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("rm user/test_file", src_dir="/home"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("touch test_file", src_dir="/home/user"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))
# print(cmd.invoke_dir("rm /home/user/test_file"))
# print(cmd.invoke_dir("ls -a user", src_dir="/home"))

# print(cmd.invoke_dir("ls user", src_dir="/home"))
# print(cmd.invoke_dir("touch test_touch", src_dir="/home/user"))
# print(cmd.invoke_dir("touch test_touch.txt", src_dir="/home/user"))
# print(cmd.invoke_dir("touch user/test_touch2.txt", src_dir="/home"))
# print(cmd.invoke_dir("touch /home/user/test_touch3.txt"))
# print(cmd.invoke_dir("ls user", src_dir="/home"))

# print(cmd.invoke_network("arp"))
# print(cmd.invoke_network("arp -d non_existend"))
# print(cmd.invoke_network("arp -d _gateway"))
# print(cmd.invoke_network("arp"))
# print(cmd.invoke_network("ip a"))

# for n, line in enumerate(cmd.invoke_network("ping 1.1.1.1")):
#    print(line)
#    if n > 1 or n < 5:
#        time.sleep(1)

# print(cmd.invoke_network("arp"))

# TODO not working properly yet with colors
# print(cmd.invoke_dir("ls -alr user", src_dir="/home"))
# print(cmd.invoke_dir("ls -ar", src_dir="/"))

# print(cmd.invoke_process("ps", "tty2", "user1"))
# print(cmd.invoke_process("ps -af", "tty2", "user1"))
# print(cmd.invoke_process("kill 5410", "pts/2", "52471"))
# print(cmd.invoke_process("killall bash", "pts/2", "52471"))
# print(cmd.invoke_process("ps -f", "tty2", "user1"))
# print(cmd.invoke_process("ps -ef", "tty2", "user1"))
# (cmd.invoke_process("ps ax", "tty2", "user1"))
# print(cmd.invoke_process("ps x", "tty2", "user1"))
# print(cmd.invoke_process("ps aux", "tty2", "user1"))
