"""
Audio Extractor APIのエントリーポイント。

このモジュールは、FastAPIアプリケーションを初期化し、
ミドルウェア、例外ハンドラー、ルーターを登録します。
"""

from fastapi import FastAPI
from api.v1.endpoints import extract_audio
from infrastructure.framework.exception_handlers import get_exception_handlers
from infrastructure.framework.middlewares import setup_middlewares

app = FastAPI(
    title="Audio Extractor API",
    version="1.0.0"
)

# ミドルウェアの登録
setup_middlewares(app)

# 例外ハンドラーの登録
for exception, handler in get_exception_handlers():
    app.add_exception_handler(exception, handler)

# ルーターの登録
app.include_router(extract_audio.router, prefix="/api/v1")
