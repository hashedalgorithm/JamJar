from core.ebpf import EBPF
import os
from utils.logger import Logger
import traceback


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
        by Sanjay Kumar Kumaravelan, Nivedhidha       ⣿⡇⠀⠀⠙⠛⢻⣷⣾⡟⠛⠋⠀⠀⣿⠀⢸⣿
        Ilangovan & Monisha Vannamuthu                ⣿⡇⠀   ⡏   ⢹⠀⠀⠀⠀⣿⠀⢸⣿
                                                      ⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠀⣸⡟
                                                       ⠛⢷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡾⠛
    """
    )


if __name__ == "__main__":

    try:
        logger = Logger(__name__).logger
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
        logger.error(f"Error: {e}\n{traceback.format_exc()}")
