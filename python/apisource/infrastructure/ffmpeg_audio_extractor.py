import ffmpeg
from pathlib import Path
from typing import List
import asyncio

from domain.interfaces.audio_extractor_interface import IAudioExtractor, AudioExtractionFailedException

class FFmpegAudioExtractor(IAudioExtractor):
    """
    FFmpegを使用して音声トラックを抽出するクラス。

    IAudioExtractorインターフェースを実装します。
    """

    def __get_audio_tracks(self, video_path: str):
        """
        ビデオファイルから利用可能な音声トラックを取得します。

        Args:
            video_path (str): 音声トラックを取得するビデオファイルのパス。

        Returns:
            list: 利用可能な音声トラックのインデックスリスト。
        """
        probe = ffmpeg.probe(video_path, v='error', select_streams='a', show_entries='stream=index')
        return [stream['index'] for stream in probe['streams']]

    async def __extract_audio(self, video_path: str, output_path: Path, track_index: int):
        """
        指定された音声トラックを抽出して保存します。

        Args:
            video_path (str): 音声を抽出するビデオファイルのパス。
            output_path (Path): 抽出した音声を保存するパス。
            track_index (int): 抽出する音声トラックのインデックス。
        """
        process = (
            ffmpeg.input(video_path)
            .output(str(output_path), acodec='aac', audio_bitrate='192k', map=f"0:{track_index}")
            .run_async(quiet=True)
        )
        await asyncio.to_thread(process.wait)

    async def extract_all_audio(self, video_path: str, output_dir: Path) -> List[Path]:
        """
        ビデオファイルからすべての音声トラックを抽出し、指定されたディレクトリに保存します。

        Args:
            video_path (str): 音声を抽出するビデオファイルのパス。
            output_dir (Path): 抽出した音声を保存するディレクトリ。

        Returns:
            List[Path]: 抽出された音声ファイルのパスのリスト。

        Raises:
            AudioExtractionFailedException: 音声抽出に失敗した場合。
        """
        try:
            track_indices = self.__get_audio_tracks(video_path)
            audio_files = []
            tasks = []

            for track_index in track_indices:
                output_path = output_dir / f"audio_track_{track_index}.aac"
                tasks.append(self.__extract_audio(video_path, output_path, track_index))
                audio_files.append(output_path)

            await asyncio.gather(*tasks)

            return audio_files
        except Exception as e:
            raise AudioExtractionFailedException() from e
