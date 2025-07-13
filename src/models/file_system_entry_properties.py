import datetime
from typing import Literal


class FileSystemEntryProperties:

    def __init__(
        self,
        name: str,
        perm: str = "-rwxrwxrwx",
        xxx: str = "1",
        owner: str = "root",
        group: str = "root",
        size: str = 4096,
        extension: str = "",
        parent: str = "",
        created_month: datetime = datetime.datetime.now(),
        created_day: datetime = datetime.datetime.now(),
        created_time: datetime = datetime.datetime.now(),
        ctime: str = datetime.datetime.now(),
        mtime: str = datetime.datetime.now(),
    ) -> None:

        self.perm: str = perm
        self.xxx: str = xxx
        self.owner: str = owner
        self.group: str = group
        self.size: str = size
        self.created_month: datetime = created_month
        self.created_day: datetime = created_day
        self.created_time: datetime = created_time
        self.name: str = name
        self.extension: str = extension
        self.parent: str = parent
        self.path: str = f"{name}{"." if extension else ""}{extension}"
        self.ctime: datetime = ctime
        self.mtime: datetime = mtime

    def get_link(self) -> int:
        return 2

    def formatted_time(
        self,
        attribute: Literal[
            "created_month", "created_day", "created_time", "ctime", "mtime"
        ],
        format: str,
    ) -> str:
        if attribute == "created_month":
            return self.created_month.strftime(format)
        elif attribute == "created_day":
            return self.created_day.strftime(format)
        elif attribute == "created_time":
            return self.created_time.strftime(format)
        elif attribute == "ctime":
            return self.ctime.strftime(format)
        elif attribute == "mtime":
            return self.mtime.strftime(format)

    def get_created_day(self, format: str = "%d") -> str:
        format = format or "%d"
        return self.formatted_time("created_day", format)

    def get_created_month(self, format: str = "%b") -> str:
        format = format or "%b"
        return self.formatted_time("created_month", format)

    def get_created_time(self, format: str = "%H:%M") -> str:
        format = format or "%H:%M"
        return self.formatted_time("created_time", format)

    def get_ctime(self, format: str = "%H:%M") -> str:
        format = format or "%H:%M"
        return self.formatted_time("ctime", format)

    def get_mtime(self, format: str = "%H:%M") -> str:
        format = format or "%H:%M"
        return self.formatted_time("mtime", format)

    def __repr__(self) -> str:
        return (
            f"FileSystemEntryProperties("
            f"name={self.name!r},{self.extension!r}, perm={self.perm!r}, xxx={self.xxx!r}, "
            f"owner={self.owner!r}, group={self.group!r}, size={self.size!r}, "
            f"created_month={self.created_month!r}, created_day={self.created_day!r}, "
            f"created_time={self.created_time!r}, parent={self.parent!r})"
        )
