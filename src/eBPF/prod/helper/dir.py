import datetime
from typing import Union, Optional

from helper.file import File


class Dir(File):
    content: dict[str, Union["Dir", File]] = {}

    def __init__(
        self,
        name: str,
        perm: str = "-rwxrwxrwx",
        xxx: str = "1",
        owner: str = "root",
        group: str = "root",
        size: str = 4096,
        created_month: str = datetime.datetime.now().strftime("%b"),
        created_day: str = datetime.datetime.now().strftime("%d"),
        created_time: str = datetime.datetime.now().strftime("%H:%M"),
        parent: Optional["Dir"] = None,
    ) -> None:

        self.content = {}
        self.perm = perm
        self.xxx = xxx
        self.owner = owner
        self.group = group
        self.size = size
        self.created_month = created_month
        self.created_day = created_day
        self.created_time = created_time
        self.name = name
        self.file_type = "directory"
        self.parent = parent
