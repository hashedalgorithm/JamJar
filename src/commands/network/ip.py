from commands.base import CommandBase
from models.route import ROUTE
from models.interface import INTERFACE


class IP(CommandBase):
    def __init__(self) -> None:
        super().__init__("ip")
        
    def run(self) -> str | None:
        raise Exception("IP not implemented yet!")
    
    def ip(self, args):

        output = ""

        args_str = "".join(args)
        a = "a" in args_str or "addr" in args_str
        r = "r" in args_str or "route" in args_str
        add = "add" in args_str
        delete = "del" in args_str

        if a:
            if add:
                self.interfaces[args[-1]].add_ip(args[-3])

            elif delete:
                self.interfaces[args[-1]].del_ip(args[-3])

            else:
                for n, entry in enumerate(self.interfaces):
                    output += f"{n+1}: {str(self.interfaces[entry])}\n"

        if r:
            if add:
                self.routes.append(
                    ROUTE(inet_to=args[-3], interface=self.interfaces[args[-1]])
                )

            elif delete:
                for x, route in enumerate(self.routes):
                    if args[-1] in route.interface.names and route.inet_to in args[-3]:
                        self.routes.pop(x)
                        break
            else:
                for entry in self.routes:
                    output += str(entry) + "\n"

        return output.strip("\n")