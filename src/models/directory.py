from __future__ import annotations
from .file_system_entry_properties import FileSystemEntryProperties
from .file import File
from typing import Optional


class Directory(FileSystemEntryProperties):
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
        doc.parent = f"{self.parent}{self.name}/"

    def delete_something(self, names: list[str]) -> None:
        for n in names:
            if n in self.children:
                del self.children[n]

    def clear(self) -> None:
        self.children = {}

    def get_path(self):
        return f"{self.parent}{self.name}"

    def get_children(self) -> list[File | "Directory"]:
        return [child for child in self.children]

    def find_entry(self, name: str) -> File | "Directory" | None:
        for child in self.children.values():
            print("Find:", child.name, name)
            if child.name == name:
                return child
        return None

    def get_link(
        self,
    ) -> int:
        count = 2
        for child in self.children.values():
            if child.extension == "dir":
                count += 1
        return count

    def __repr__(self) -> str:
        return f"<Directory name='{self.name}' children={[child for child in self.children]}>"
