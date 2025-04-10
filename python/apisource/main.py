from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from babel.support import Translations
import os

from api.v1.endpoints import extract_audio
from domain.interfaces.audio_extractor_interface import AudioTrackRetrievalException, AudioExtractionFailedException

app = FastAPI(
    title="Audio Extractor API",
    version="1.0.0"
)

# 言語設定
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'translations')
DEFAULT_LANGUAGE = 'en'

@app.middleware("http")
async def add_translation_middleware(request: Request, call_next):
    lang = request.headers.get("Accept-Language", DEFAULT_LANGUAGE)
    translations = Translations.load(LOCALE_DIR, [lang])
    request.state.translations = translations
    response = await call_next(request)
    return response

# 例外処理
@app.exception_handler(AudioTrackRetrievalException)
async def audio_track_retrieval_exception_handler(request: Request, exc: AudioTrackRetrievalException):
    _ = request.state.translations.gettext
    message = _("error.audio_track_retrieval")
    return JSONResponse(status_code=500, content={"message": message})

@app.exception_handler(AudioExtractionFailedException)
async def audio_extraction_failed_exception_handler(request: Request, exc: AudioExtractionFailedException):
    _ = request.state.translations.gettext
    message = _("error.audio_extraction_failed")
    return JSONResponse(status_code=500, content={"message": message})

# ルーターの登録
app.include_router(extract_audio.router, prefix="/api/v1")
