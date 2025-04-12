from abc import ABC, abstractmethod
from pathlib import Path

class IArchiver(ABC):
    """
    アーカイバのインターフェース。

    ファイルをアーカイブ形式に変換するためのメソッドを定義します。
    """

    @abstractmethod
    def create_archive(self, files: list[Path], archive_path: str) -> bytes:
        """
        ファイルをアーカイブにまとめます。

        Args:
            files (list[Path]): アーカイブするファイルのリスト。
            archive_path (str): アーカイブファイルの保存先パス。

        Returns:
            bytes: アーカイブされたデータのバイト列。
        """
        pass
