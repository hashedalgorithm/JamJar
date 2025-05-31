from core.ebpf import EBPF
import os


# ASCII art created with https://emojicombos.com/skull-ascii-art,
# https://emojicombos.com/mason-jar-ascii-art,
# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=JamJar


def ascii_art():
    print(
        r"""
                                                        ⣴⠟⠛⠛⠛⠛⠛⠛⠛⠛⢛⣛⣻⣦
                                                        ⣿⣶⣶⡶⠀⠀⠛⠛⠋⠉⠉⠉⠉⣿
     ____                     ____                     ⠘⠿⢿⡿⠿⠿⠿⠿⠿⠿⠿⠿⢿⡿⠿⠃
    |    |____    _____      |    |____ _______        ⣠⣶⠿⠃⠀⠀⠀⠀⠀⠀⣶⡀⠘⠿⣶⣄
    |    \__  \  /     \     |    \__  \\_  __ \      ⣼⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢷⣄⠈⢻⣧
/\__|    |/ __ \|  Y Y  \/\__|    |/ __ \|  | \/      ⣿⡇⠀⠀⠀⢀⣠⣤⣤⣄⡀⠀⠀⠀⣿⠀⢸⣿
\________(____  /__|_|  /\________(____  /__|         ⣿⡇⠀⠀⣴⣿⣿⣿⣿⣿⣿⣦⠀⠀⣿⠀⢸⣿
              \/      \/               \/             ⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⠀⢸⣿
        © Jamjar v2.0                                 ⣿⡇⠀⠀⣇⠈⠉⡿⢿⠉⠁⣸⠀⠀⣿⠀⢸⣿
        by Sanjay Kumar Kumaravelan, Niveditha        ⣿⡇⠀⠀⠙⠛⢻⣷⣾⡟⠛⠋⠀⠀⣿⠀⢸⣿
        Illangovan & Monisha Vanamuthu                ⣿⡇⠀   ⡏  ⢹⠀⠀⠀⠀⣿⠀⢸⣿
                                                      ⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠀⣸⡟
                                                       ⠛⢷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡾⠛
    """
    )


if __name__ == "__main__":

    ascii_art()

    # Initialize BPF
    ebpf = EBPF(ebpf_path=os.path.join(os.path.dirname(__file__), "bpf/v1.0.c"))

    # Loop with callback to print_event
    ebpf.bpf["events"].open_perf_buffer(ebpf.proc_event)

    print("[+] Jamjar is running... Press Ctrl+C to exit.")

    while True:
        try:
            ebpf.bpf.perf_buffer_poll()

        except Exception as e:
            print(f"[!] Error: {e}")

        except KeyboardInterrupt:
            exit()

        finally:
            ebpf.quit_debugger()
