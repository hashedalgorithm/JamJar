from __future__ import annotations
from typing import Union, Optional

from helper.file import StorageEntryProperties, File


class Dir(StorageEntryProperties):
    content: dict[str, Union["Dir", "File"]] = {}

    def __init__(
        self,
        name: str,
        parent: Optional["Dir"] = None,
        **kwargs: Optional[dict[str, str]],
    ) -> None:

        super().__init__(name=name, file_type="directory", **kwargs)
        self.parent = parent
