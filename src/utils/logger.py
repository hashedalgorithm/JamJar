import logging


class Logger:

    def __init__(self):
        full_name = f"{self.__module__}.{self.__class__.__name__}"
        self.logger = logging.getLogger(full_name)

        # Avoid duplicate handlers if the logger is already configured
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)  # Set the base log level

            # Create handlers
            info_handler = logging.StreamHandler()
            file_handler = logging.FileHandler("jamjar.log", mode="a")
            error_handler = logging.StreamHandler()
            critical_error_handler = logging.StreamHandler()
            fatal_error_handler = logging.StreamHandler()
            warning_handler = logging.StreamHandler()

            # Create formatters for different log levels
            info_formatter = logging.Formatter("[+] %(asctime)s - %(message)s")
            error_formatter = logging.Formatter(
                "[!] %(asctime)s - %(name)s - %(message)s"
            )
            critical_error_formatter = logging.Formatter(
                "[!!] %(asctime)s - %(name)s - %(message)s"
            )
            fatal_error_formatter = logging.Formatter(
                "[!!!] %(asctime)s - %(name)s - %(message)s"
            )
            warning_formatter = logging.Formatter("[-] %(asctime)s - %(message)s")
            file_formatter = logging.Formatter(
                "[+] %(asctime)s - %(name)s - %(message)s"
            )

            # Assign formatters to handlers
            info_handler.setFormatter(info_formatter)
            error_handler.setFormatter(error_formatter)
            critical_error_handler.setFormatter(critical_error_formatter)
            fatal_error_handler.setFormatter(fatal_error_formatter)
            warning_handler.setFormatter(warning_formatter)
            file_handler.setFormatter(file_formatter)

            # Use a filter to apply the error formatter only for ERROR and above
            info_handler.setLevel(logging.INFO)
            error_handler.setLevel(logging.ERROR)
            critical_error_handler.setLevel(logging.CRITICAL)
            fatal_error_handler.setLevel(logging.FATAL)
            warning_handler.setLevel(logging.WARNING)

            # Add handlers to the logger
            self.logger.addHandler(info_handler)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(error_handler)
            self.logger.addHandler(critical_error_handler)
            self.logger.addHandler(fatal_error_handler)
            self.logger.addHandler(warning_handler)
