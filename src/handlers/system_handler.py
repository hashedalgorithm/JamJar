class SystemHandler:

    def __init__(self):
        pass

    def handle(self, command: str, args: list):

        match command:
            case "df":
                return self.df()

            case "history":
                return self.history()

            case "php":
                return self.php()

            case "uname":
                return self.uname()

            case "whoami":
                return self.whoami()

            case "w":
                return self.w()

            case "id":
                return self.id()

            case "last":
                return self.last()

            case "uptime":
                return self.uptime()

            case _:
                print(f"Command '{command}' not recognized by SystemHandler.")
                return None

    def df(self):
        # TODO: Implement df command
        pass

    def history(self):
        # TODO: Implement history command
        print("history not implemented yet")
        return None

    def php(self):
        # TODO: Implement php command
        print("php not implemented yet")
        return None

    def uname(self):
        # TODO: Implement uname command
        print("uname not implemented yet")
        return None

    def whoami(self):
        # TODO: Implement whoami command
        print("whoami not implemented yet")
        return None

    def w(self):
        # TODO: Implement w command
        print("w not implemented yet")
        return None

    def id(self):
        # TODO: Implement id command
        print("id not implemented yet")
        return None

    def last(self):
        # TODO: Implement last command
        print("last not implemented yet")
        return None

    def uptime(self):
        # TODO: Implement uptime command
        print("uptime not implemented yet")
        return None
