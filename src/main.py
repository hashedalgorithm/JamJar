from core.ebpf import EBPF
import os, logging


def ascii_art():
    # ASCII art created with https://emojicombos.com/skull-ascii-art,
    # https://emojicombos.com/mason-jar-ascii-art,
    # https://patorjk.com/software/taag/#p=display&f=Graffiti&t=JamJar

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

    try:
        logger = logging.getLogger(__name__)
        ascii_art()

        # Initialize BPF
        ebpf = EBPF(ebpf_path=os.path.join(os.path.dirname(__file__), "bpf/v2.0.c"))
        ebpf.intialize_hook_points()

        logger.info("Listening syscalls... Press Ctrl+C to exit.")

        while True:
            ebpf.bpf.perf_buffer_poll()

    except KeyboardInterrupt:
        logger.error("Keyboard Interrupt Detected! Exiting...")
        exit(1)

    except Exception as e:
        logger.error(f"Error: {e}")
