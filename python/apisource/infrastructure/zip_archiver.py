import zipfile
from pathlib import Path

from domain.interfaces.archiver_interface import IArchiver

class ZipArchiver(IArchiver):
    def create_archive(self, files: list[Path], archive_path: str) -> bytes:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, file.name)

        with open(archive_path, 'rb') as f:
            return f.read()
