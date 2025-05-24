from __future__ import annotations
from typing import Optional, Any

from helper.file import StorageEntryProperties


class Dir(StorageEntryProperties):
    content: dict[str, Any] = {}

    def __init__(
        self,
        name: str,
        parent: Optional[Any] = None,
        **kwargs: Optional[dict[str, str]],
    ) -> None:

        super().__init__(name=name, file_type="directory", **kwargs)
        self.parent = parent
