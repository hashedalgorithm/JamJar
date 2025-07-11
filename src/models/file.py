from .file_system_entry_properties import FileSystemEntryProperties
from typing import Optional


class File(FileSystemEntryProperties):
    def __init__(
        self,
        name: str,
        file_type: str = "",
        content: str = "",
        **kwargs: Optional[dict[str, str]],
    ) -> None:

        super().__init__(name=name, **kwargs)
        self.content = content
        self.file_type = file_type

    def write(self, content: str) -> None:
        self.content = content

    def append(self, content: str) -> None:
        self.content += content

    def read(self) -> str:
        return self.content

    def rename(self, new_name: str) -> None:
        self.name = new_name

    def __repr__(self) -> str:
        return f"File(name={self.name!r}, file_type={self.file_type!r}, content={self.content!r})"
