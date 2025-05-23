import logging
import os
from logging.handlers import RotatingFileHandler
from fastapi import Depends
from domain.interfaces.archiver_interface import IArchiver
from domain.interfaces.audio_extractor_interface import IAudioExtractor
from infrastructure.ffmpeg_audio_extractor import FFmpegAudioExtractor
from infrastructure.zip_archiver import ZipArchiver
from service.audio_extractor_service import AudioExtractorService
from datetime import datetime
from pathlib import Path

# ログディレクトリの作成
LOG_DIR = Path(os.getcwd()) / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

class IndentedFormatter(logging.Formatter):
    """
    ログメッセージをインデントしてフォーマットするカスタムフォーマッター。

    Attributes:
        fmt (str): ログメッセージのフォーマット。
        datefmt (str): 日付のフォーマット。
        tz (datetime.tzinfo): タイムゾーン情報。
    """
    def __init__(self, fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.tz = datetime.now().astimezone().tzinfo

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        return dt.strftime(self.datefmt)

    def format(self, record):
        original_message = super().format(record)
        indented_message = "\n  ".join(original_message.splitlines())
        return indented_message

# アクセスロガーの設定
access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)
access_log_file = os.path.join(LOG_DIR, "access.log")
access_file_handler = RotatingFileHandler(access_log_file, maxBytes=10**6, backupCount=5)
access_formatter = IndentedFormatter()
access_file_handler.setFormatter(access_formatter)
access_logger.addHandler(access_file_handler)
def get_access_logger() -> logging.Logger:
    """
    アクセスロガーのインスタンスを提供します。

    Returns:
        logging.Logger: アクセスロガーのインスタンス。
    """
    return access_logger

# エラーロガーの設定
error_logger = logging.getLogger("error")
error_logger.setLevel(logging.ERROR)
error_log_file = os.path.join(LOG_DIR, "error.log")
error_file_handler = RotatingFileHandler(error_log_file, maxBytes=10**6, backupCount=5)
error_formatter = IndentedFormatter()
error_file_handler.setFormatter(error_formatter)
error_logger.addHandler(error_file_handler)
def get_error_logger() -> logging.Logger:
    """
    エラーロガーのインスタンスを提供します。

    Returns:
        logging.Logger: エラーロガーのインスタンス。
    """
    return error_logger

def get_audio_extractor() -> IAudioExtractor:
    """
    音声抽出器のインスタンスを提供します。

    Returns:
        IAudioExtractor: 音声抽出器のインスタンス。
    """
    return FFmpegAudioExtractor()

def get_archiver() -> IArchiver:
    """
    アーカイバのインスタンスを提供します。

    Returns:
        IArchiver: アーカイバのインスタンス。
    """
    return ZipArchiver()

def get_audio_extractor_service(
    extractor: IAudioExtractor = Depends(get_audio_extractor),
    archiver: IArchiver = Depends(get_archiver)
) -> AudioExtractorService:
    """
    AudioExtractorServiceのインスタンスを提供します。

    Args:
        extractor (IAudioExtractor): 音声抽出器の依存関係。
        archiver (IArchiver): アーカイバの依存関係。

    Returns:
        AudioExtractorService: AudioExtractorServiceのインスタンス。
    """
    return AudioExtractorService(extractor, archiver)
