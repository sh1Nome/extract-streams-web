import zipfile
from pathlib import Path

from domain.interfaces.archiver_interface import IArchiver

class ZipArchiver(IArchiver):
    """
    ZIP形式でファイルをアーカイブするクラス。

    IArchiverインターフェースを実装します。
    """

    def create_archive(self, files: list[Path], archive_path: str) -> bytes:
        """
        ファイルをZIPアーカイブにまとめます。

        Args:
            files (list[Path]): アーカイブするファイルのリスト。
            archive_path (str): アーカイブファイルの保存先パス。

        Returns:
            bytes: アーカイブされたデータのバイト列。
        """
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, file.name)

        with open(archive_path, 'rb') as f:
            return f.read()
