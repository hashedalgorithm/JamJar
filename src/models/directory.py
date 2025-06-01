from .file_system import StorageEntryProperties
from .file import File
from typing import Optional


class Directory(StorageEntryProperties):
    def __init__(
        self,
        name: str,
        **kwargs: Optional[dict[str, str]],
    ) -> None:

        super().__init__(name=name, **kwargs)
        self.children: dict[str, File | "Directory"] = {}

    def add(self, doc: File) -> None:
        if doc.name in self.children:
            raise ValueError(f"'{doc.name}' already exists in '{self.name}'.")
        self.children[doc.name] = doc
        doc.parent = self

    def delete_something(self, names: list[str]) -> None:
        for n in names:
            if n in self.children:
                del self.children[n]

    def clear(self) -> None:
        self.children = {}
