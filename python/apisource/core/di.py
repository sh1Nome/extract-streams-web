from fastapi import Depends
from domain.interfaces.archiver_interface import IArchiver
from domain.interfaces.audio_extractor_interface import IAudioExtractor
from infrastructure.ffmpeg_audio_extractor import FFmpegAudioExtractor
from infrastructure.zip_archiver import ZipArchiver
from service.audio_extractor_service import AudioExtractorService

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
