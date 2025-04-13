import time
from fastapi import Request
from babel.support import Translations
import os
import logging

LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../translations'))  # パスを修正
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

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))  # パスを修正
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,  # ログレベルを設定
    filename=os.path.join(LOG_DIR, "access.log"),
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
access_logger = logging.getLogger("access")

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

    access_logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
    )
    return response

def get_middlewares():
    """
    ミドルウェアのリストを返す関数。
    """
    return [add_translation_middleware, log_requests_middleware]