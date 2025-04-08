from fastapi import Depends
from domain.interfaces.archiver_interface import IArchiver
from domain.interfaces.audio_extractor_interface import IAudioExtractor
from infrastructure.ffmpeg_audio_extractor import FFmpegAudioExtractor
from infrastructure.zip_archiver import ZipArchiver
from service.audio_extractor_service import AudioExtractorService

# AudioExtractorを提供する関数
def get_audio_extractor() -> IAudioExtractor:
    return FFmpegAudioExtractor()

# Archiverを提供する関数
def get_archiver() -> IArchiver:
    return ZipArchiver()

# AudioExtractorServiceを提供する関数
def get_audio_extractor_service(
    extractor: IAudioExtractor = Depends(get_audio_extractor),
    archiver: IArchiver = Depends(get_archiver)
) -> AudioExtractorService:
    return AudioExtractorService(extractor, archiver)
