"""
Audio Extractor APIのエントリーポイント。

このモジュールは、FastAPIアプリケーションを初期化し、
ミドルウェア、例外ハンドラー、ルーターを登録します。
"""

from fastapi import FastAPI
from api.v1.endpoints import extract_audio
from domain.interfaces.audio_extractor_interface import AudioExtractionFailedException, AudioTrackRetrievalException
from infrastructure.framework.exception_handlers import (
    audio_extraction_failed_exception_handler,
    audio_track_retrieval_exception_handler,
)
from infrastructure.framework.middlewares import add_translation_middleware, log_requests_middleware

app = FastAPI(
    title="Audio Extractor API",
    version="1.0.0"
)

# ミドルウェアの登録
app.middleware("http")(add_translation_middleware)
app.middleware("http")(log_requests_middleware)

# 例外ハンドラーの登録
app.add_exception_handler(AudioTrackRetrievalException, audio_track_retrieval_exception_handler)
app.add_exception_handler(AudioExtractionFailedException, audio_extraction_failed_exception_handler)

# ルーターの登録
app.include_router(extract_audio.router, prefix="/api/v1")
