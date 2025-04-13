import tempfile
from pathlib import Path

from domain.interfaces.archiver_interface import IArchiver
from domain.interfaces.audio_extractor_interface import IAudioExtractor

class AudioExtractorService:
    """
    音声抽出サービスクラス。

    ビデオファイルから音声を抽出し、アーカイブを作成する機能を提供します。
    """

    def __init__(self, extractor: IAudioExtractor, archiver: IArchiver):
        """
        AudioExtractorServiceを初期化します。

        Args:
            extractor (IAudioExtractor): 音声を抽出するためのインターフェース。
            archiver (IArchiver): ファイルをアーカイブするためのインターフェース。
        """
        self.extractor = extractor
        self.archiver = archiver

    async def extract(self, file_name: str, file_content: bytes):
        """
        ビデオファイルから音声を抽出し、アーカイブを作成します。

        Args:
            file_name (str): ファイル名。
            file_content (bytes): ファイルのバイトデータ。

        Returns:
            tuple: アーカイブのバイトデータとアーカイブファイル名。
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file_name).suffix) as tmp_file:
            tmp_file.write(file_content)
            tmp_file.close()

            audio_dir = Path(tmp_file.name + "_audio")
            audio_dir.mkdir(parents=True, exist_ok=True)

            audio_files = self.extractor.extract_all_audio(tmp_file.name, audio_dir)

            archive_path = tmp_file.name + "_audio.zip"
            archive_bytes = self.archiver.create_archive(audio_files, archive_path)

            return archive_bytes, Path(archive_path).name
