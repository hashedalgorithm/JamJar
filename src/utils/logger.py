import logging


class Logger:
    def __init__(self):
        full_name = f"{self.__module__}.{self.__class__.__name__}"
        self.logger = logging.getLogger(full_name)
