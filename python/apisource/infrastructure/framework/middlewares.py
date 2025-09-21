import time
from fastapi import Request
from babel.support import Translations
import os

from infrastructure.framework.di import get_access_logger
from fastapi.middleware.cors import CORSMiddleware

LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../translations'))
DEFAULT_LANGUAGE = 'en'

async def add_translation_middleware(request: Request, call_next):
    """
    翻訳ミドルウェア。

    リクエストヘッダーの"Accept-Language"に基づいて翻訳を設定します。

    Args:
        request (Request): HTTPリクエストオブジェクト。
        call_next: 次のミドルウェアまたはエンドポイントを呼び出す関数。

    Returns:
        Response: 処理されたHTTPレスポンス。
    """
    lang = request.headers.get("Accept-Language", DEFAULT_LANGUAGE)
    translations = Translations.load(LOCALE_DIR, [lang])
    request.state.translations = translations
    response = await call_next(request)
    return response

async def log_requests_middleware(request: Request, call_next):
    """
    リクエストログ記録ミドルウェア。

    各リクエストの処理時間とステータスコードをログに記録します。

    Args:
        request (Request): HTTPリクエストオブジェクト。
        call_next: 次のミドルウェアまたはエンドポイントを呼び出す関数。

    Returns:
        Response: 処理されたHTTPレスポンス。
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    get_access_logger().info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
    )
    return response

def setup_middlewares(app):
    """
    FastAPIアプリに必要な全ミドルウェアを登録する関数。
    関数型・クラス型ミドルウェアの両方を一元管理。
    Args:
        app (FastAPI): FastAPIアプリケーションインスタンス
    """
    # クラス型ミドルウェア（CORSなど）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # 関数型ミドルウェア
    app.middleware("http")(add_translation_middleware)
    app.middleware("http")(log_requests_middleware)
