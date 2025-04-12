from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class IAudioExtractor(ABC):
    @abstractmethod
    def get_audio_tracks(self, video_path: str) -> List[int]:
        pass

    @abstractmethod
    def extract_audio(self, video_path: str, output_path: Path, track_index: int) -> None:
        pass

class AudioTrackRetrievalException(Exception):
    """
    オーディオトラックの取得中に発生する例外。

    この例外は、外部サービスや内部処理でオーディオトラックを取得できなかった場合に発生します。
    """

class AudioExtractionFailedException(Exception):
    """
    オーディオ抽出処理が失敗した場合に発生する例外。

    この例外は、オーディオファイルの解析や変換中にエラーが発生した場合に発生します。
    """
