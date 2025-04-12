from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class IAudioExtractor(ABC):
    """
    音声抽出器のインターフェース。

    ビデオファイルから音声トラックを取得し、音声を抽出するためのメソッドを定義します。
    """

    @abstractmethod
    def get_audio_tracks(self, video_path: str) -> List[int]:
        """
        ビデオファイルから利用可能な音声トラックを取得します。

        Args:
            video_path (str): 音声トラックを取得するビデオファイルのパス。

        Returns:
            List[int]: 利用可能な音声トラックのインデックスリスト。
        """
        pass

    @abstractmethod
    def extract_audio(self, video_path: str, output_path: Path, track_index: int) -> None:
        """
        指定された音声トラックを抽出して保存します。

        Args:
            video_path (str): 音声を抽出するビデオファイルのパス。
            output_path (Path): 抽出した音声を保存するパス。
            track_index (int): 抽出する音声トラックのインデックス。
        """
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
