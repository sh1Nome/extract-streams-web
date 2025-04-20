from fastapi import Request
from fastapi.responses import JSONResponse

from domain.interfaces.audio_extractor_interface import AudioExtractionFailedException
from api.v1.endpoints.validation_exceptions import InvalidFileTypeException
from infrastructure.framework.di import get_error_logger

async def audio_extraction_failed_exception_handler(request: Request, exc: AudioExtractionFailedException):
    """
    AudioExtractionFailedExceptionを処理する例外ハンドラー。

    オーディオ抽出の失敗時に発生した例外を処理し、適切なエラーメッセージを含むJSONレスポンスを返します。

    Args:
        request (Request): 受信したHTTPリクエスト。
        exc (AudioExtractionFailedException): 発生した例外。

    Returns:
        JSONResponse: エラーメッセージを含むHTTPレスポンス。
    """
    get_error_logger().error(f"AudioExtractionFailedException: {exc}", exc_info=True)
    _ = request.state.translations.gettext
    message = _("error.audio_extraction_failed")
    return JSONResponse(status_code=500, content={"message": message})

async def invalid_file_type_exception_handler(request: Request, exc: InvalidFileTypeException):
    """
    InvalidFileTypeExceptionを処理する例外ハンドラー。

    動画形式でないファイルがアップロードされた場合に適切なエラーメッセージを含むJSONレスポンスを返します。

    Args:
        request (Request): 受信したHTTPリクエスト。
        exc (InvalidFileTypeException): 発生した例外。

    Returns:
        JSONResponse: エラーメッセージを含むHTTPレスポンス。
    """
    get_error_logger().error(f"InvalidFileTypeException: {exc}", exc_info=True)
    _ = request.state.translations.gettext
    message = _("error.invalid_file_type")
    return JSONResponse(status_code=400, content={"message": message})

async def generic_exception_handler(request: Request, exc: Exception):
    """
    未定義の例外を処理する汎用例外ハンドラー。

    Args:
        request (Request): 受信したHTTPリクエスト。
        exc (Exception): 発生した例外。

    Returns:
        JSONResponse: エラーメッセージを含むHTTPレスポンス。
    """
    get_error_logger().error(f"Unhandled Exception: {exc}", exc_info=True)
    _ = request.state.translations.gettext
    message = _("error.unexpected")
    return JSONResponse(status_code=500, content={"message": message})

def get_exception_handlers():
    """
    例外ハンドラーのリストを返す関数。
    """
    return [
        (AudioExtractionFailedException, audio_extraction_failed_exception_handler),
        (InvalidFileTypeException, invalid_file_type_exception_handler),
        (Exception, generic_exception_handler),
    ]