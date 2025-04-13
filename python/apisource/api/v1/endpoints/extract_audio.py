from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
import io

from infrastructure.framework.di import get_audio_extractor_service
from service.audio_extractor_service import AudioExtractorService

router = APIRouter()

@router.post("/extract_audio")
async def extract_audio(
    file: UploadFile = File(...),
    service: AudioExtractorService = Depends(get_audio_extractor_service)
):
    """
    アップロードされたファイルから音声を抽出し、ダウンロード可能なアーカイブとして返します。

    Args:
        file (UploadFile): 抽出対象の音声を含むアップロードファイル。
        service (AudioExtractorService): 音声を抽出するためのサービス。

    Returns:
        StreamingResponse: 抽出された音声アーカイブを含むレスポンス。
    """
    file_content = await file.read()
    archive_content, archive_name = await service.extract(file.filename, file_content)
    return StreamingResponse(io.BytesIO(archive_content), media_type="application/zip", headers={
        "Content-Disposition": f"attachment; filename={archive_name}"
    })
