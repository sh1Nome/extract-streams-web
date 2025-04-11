from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from babel.support import Translations
import os
import logging
import time

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

# ログディレクトリの設定
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)  # ディレクトリが存在しない場合は作成

# アクセスログの設定
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(LOG_DIR, "access.log"),
    filemode="a",  # "a"は追記モード
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("access")

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
    )
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
