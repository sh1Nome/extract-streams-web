import logging
import os
from logging.handlers import RotatingFileHandler
from fastapi import Depends
from domain.interfaces.archiver_interface import IArchiver
from domain.interfaces.audio_extractor_interface import IAudioExtractor
from infrastructure.ffmpeg_audio_extractor import FFmpegAudioExtractor
from infrastructure.zip_archiver import ZipArchiver
from service.audio_extractor_service import AudioExtractorService

# ログ設定
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
os.makedirs(LOG_DIR, exist_ok=True)


# アクセスロガーの設定
access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)
log_file = os.path.join(LOG_DIR, "access.log")
file_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
access_logger.addHandler(file_handler)

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
log_file = os.path.join(LOG_DIR, "error.log")
file_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)

class IndentedFormatter(logging.Formatter):
    def format(self, record):
        original_message = super().format(record)
        indented_message = "\n  ".join(original_message.splitlines())
        return indented_message

formatter = IndentedFormatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
error_logger.addHandler(file_handler)

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
