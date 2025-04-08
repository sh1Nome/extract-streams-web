from abc import ABC, abstractmethod
from pathlib import Path

class IArchiver(ABC):
    @abstractmethod
    def create_archive(self, files: list[Path], archive_path: str) -> bytes:
        pass
