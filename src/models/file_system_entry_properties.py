import datetime


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
        created_month: str = datetime.datetime.now().strftime("%b"),
        created_day: str = datetime.datetime.now().strftime("%d"),
        created_time: str = datetime.datetime.now().strftime("%H:%M"),
    ) -> None:

        self.perm: str = perm
        self.xxx: str = xxx
        self.owner: str = owner
        self.group: str = group
        self.size: str = size
        self.created_month: str = created_month
        self.created_day: str = created_day
        self.created_time: str = created_time
        self.name: str = name
        self.extension: str = extension
        self.parent: str = parent
        self.path: str = f"{name}{"." if extension else ""}{extension}"

    def __repr__(self) -> str:
        return (
            f"FileSystemEntryProperties("
            f"name={self.name!r},{self.extension!r}, perm={self.perm!r}, xxx={self.xxx!r}, "
            f"owner={self.owner!r}, group={self.group!r}, size={self.size!r}, "
            f"created_month={self.created_month!r}, created_day={self.created_day!r}, "
            f"created_time={self.created_time!r}, parent={self.parent!r})"
        )
