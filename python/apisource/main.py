from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from babel.support import Translations
import os

from api.v1.endpoints import extract_audio
from core.extract_audio_exception import ExtractAudioException

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

@app.exception_handler(ExtractAudioException)
async def custom_exception_handler(request: Request, exc: ExtractAudioException):
    _ = request.state.translations.gettext
    message = _(exc.message_key).format(**exc.kwargs)
    return JSONResponse(status_code=500, content={"message": message})

app.include_router(extract_audio.router, prefix="/api/v1")
