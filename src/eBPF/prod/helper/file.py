import datetime
from typing import Optional

from helper.dir import Dir


class File:

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
        file_type: str = "",
        parent: Optional[Dir] = None,
    ) -> None:

        self.perm = perm
        self.xxx = xxx
        self.owner = owner
        self.group = group
        self.size = size
        self.created_month = created_month
        self.created_day = created_day
        self.created_time = created_time
        self.name = name
        self.file_type = file_type
        self.parent = parent
