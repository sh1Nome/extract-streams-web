from fastapi import FastAPI

from api.v1.endpoints import extract_audio
from api.v1.exception_handler import general_exception_handler

app = FastAPI(
    title="Audio Extractor API",
    version="1.0.0"
)

# 例外ハンドラーをFastAPIに登録
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(extract_audio.router, prefix="/api/v1")
