from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
import io

from infrastructure.ffmpeg_audio_extractor import FFmpegAudioExtractor
from infrastructure.zip_archiver import ZipArchiver
from service.audio_extractor_service import AudioExtractorService

router = APIRouter()

def get_audio_extractor_service():
    extractor = FFmpegAudioExtractor()
    archiver = ZipArchiver()
    return AudioExtractorService(extractor, archiver)

@router.post("/extract_audio")
async def extract_audio(
    file: UploadFile = File(...),
    service: AudioExtractorService = Depends(get_audio_extractor_service)
):
    try:
        archive_content, archive_name = await service.extract(file)
        return StreamingResponse(io.BytesIO(archive_content), media_type="application/zip", headers={
            "Content-Disposition": f"attachment; filename={archive_name}"
        })
    except Exception as e:
        return {"error": str(e)}
