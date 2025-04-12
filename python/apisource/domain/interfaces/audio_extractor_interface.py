from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class IAudioExtractor(ABC):
    """
    音声抽出器のインターフェース。

    ビデオファイルから音声トラックを取得し、音声を抽出するためのメソッドを定義します。
    """

    @abstractmethod
    def extract_all_audio(self, video_path: str, output_dir: Path) -> List[Path]:
        """
        ビデオファイルからすべての音声トラックを抽出し、指定されたディレクトリに保存します。

        Args:
            video_path (str): 音声を抽出するビデオファイルのパス。
            output_dir (Path): 抽出した音声を保存するディレクトリ。

        Returns:
            List[Path]: 抽出された音声ファイルのパスのリスト。
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
