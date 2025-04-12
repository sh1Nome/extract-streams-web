import tempfile
from pathlib import Path
from fastapi import UploadFile

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

    async def extract(self, file: UploadFile):
        """
        アップロードされたビデオファイルから音声を抽出し、アーカイブを作成します。

        Args:
            file (UploadFile): 音声を抽出する対象のビデオファイル。

        Returns:
            tuple: アーカイブのバイトデータとアーカイブファイル名。
        """
        video_content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_content)
            tmp_file.close()

            audio_dir = Path(tmp_file.name + "_audio")
            audio_dir.mkdir(parents=True, exist_ok=True)

            audio_tracks = self.extractor.get_audio_tracks(tmp_file.name)
            audio_files = []

            for i, track_index in enumerate(audio_tracks, start=1):
                output_path = audio_dir / f"audio_{i}.m4a"
                self.extractor.extract_audio(tmp_file.name, output_path, track_index)
                audio_files.append(output_path)

            archive_path = tmp_file.name + "_audio.zip"
            archive_bytes = self.archiver.create_archive(audio_files, archive_path)

            return archive_bytes, Path(archive_path).name
