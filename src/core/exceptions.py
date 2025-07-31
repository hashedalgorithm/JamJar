class DelegateProcess(Exception):
    """
    Raised to indicate that the command should be handled by the system's
    default process, not by the custom handler.
    """

    pass
