from fastapi import Request
from fastapi.responses import JSONResponse

from domain.interfaces.audio_extractor_interface import AudioExtractionFailedException, AudioTrackRetrievalException
from api.v1.endpoints.validation_exceptions import InvalidFileTypeException
from infrastructure.framework.di import get_error_logger

# エラーログ用のロガーを設定
error_logger = get_error_logger()

async def audio_track_retrieval_exception_handler(request: Request, exc: AudioTrackRetrievalException):
    """
    AudioTrackRetrievalExceptionを処理する例外ハンドラー。

    オーディオトラックの取得中に発生した例外を処理し、適切なエラーメッセージを含むJSONレスポンスを返します。

    Args:
        request (Request): 受信したHTTPリクエスト。
        exc (AudioTrackRetrievalException): 発生した例外。

    Returns:
        JSONResponse: エラーメッセージを含むHTTPレスポンス。
    """
    error_logger.error(f"AudioTrackRetrievalException: {exc}", exc_info=True)
    _ = request.state.translations.gettext
    message = _("error.audio_track_retrieval")
    return JSONResponse(status_code=500, content={"message": message})

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
    error_logger.error(f"AudioExtractionFailedException: {exc}", exc_info=True)
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
    error_logger.error(f"InvalidFileTypeException: {exc}", exc_info=True)
    _ = request.state.translations.gettext
    message = _("error.invalid_file_type")
    return JSONResponse(status_code=400, content={"message": message})

def get_exception_handlers():
    """
    例外ハンドラーのリストを返す関数。
    """
    return [
        (AudioTrackRetrievalException, audio_track_retrieval_exception_handler),
        (AudioExtractionFailedException, audio_extraction_failed_exception_handler),
        (InvalidFileTypeException, invalid_file_type_exception_handler),
    ]