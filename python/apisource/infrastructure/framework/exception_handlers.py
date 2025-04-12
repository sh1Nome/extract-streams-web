from fastapi import Request
from fastapi.responses import JSONResponse

from domain.interfaces.audio_extractor_interface import AudioExtractionFailedException, AudioTrackRetrievalException

async def audio_track_retrieval_exception_handler(request: Request, exc: AudioTrackRetrievalException):
    """
    ハンドラー: AudioTrackRetrievalException を処理します。

    このハンドラーは、オーディオトラックの取得中に発生した例外を処理し、
    適切なエラーメッセージを含むJSONレスポンスを返します。

    引数:
        request (Request): 受信したHTTPリクエスト。
        exc (AudioTrackRetrievalException): 発生した例外。

    戻り値:
        JSONResponse: エラーメッセージを含むHTTPレスポンス。
    """
    _ = request.state.translations.gettext
    message = _("error.audio_track_retrieval")
    return JSONResponse(status_code=500, content={"message": message})

async def audio_extraction_failed_exception_handler(request: Request, exc: AudioExtractionFailedException):
    """
    ハンドラー: AudioExtractionFailedException を処理します。

    このハンドラーは、オーディオ抽出の失敗時に発生した例外を処理し、
    適切なエラーメッセージを含むJSONレスポンスを返します。

    引数:
        request (Request): 受信したHTTPリクエスト。
        exc (AudioExtractionFailedException): 発生した例外。

    戻り値:
        JSONResponse: エラーメッセージを含むHTTPレスポンス。
    """
    _ = request.state.translations.gettext
    message = _("error.audio_extraction_failed")
    return JSONResponse(status_code=500, content={"message": message})