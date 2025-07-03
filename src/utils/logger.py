import logging


class Logger:

    # Global logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Default log level
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
        handlers=[
            logging.StreamHandler(),  # Output logs to the console
            logging.FileHandler("jamjar.log", mode="a"),  # Save logs to a file
        ],
    )

    def __init__(self):
        full_name = f"{self.__module__}.{self.__class__.__name__}"
        self.logger = logging.getLogger(full_name)
