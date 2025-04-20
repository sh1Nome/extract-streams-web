"""
このモジュールは、FastAPIアプリケーションのテストケースを含んでいます。
FastAPIのTestClientを使用してリクエストをシミュレートし、レスポンスを検証します。
"""

from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock
from main import app
from infrastructure.framework.di import get_audio_extractor, get_archiver

client = TestClient(app)


def test_extract_audio_valid_file():
    """
    有効な動画ファイルを使用してextract_audioエンドポイントをテストします。

    このテストでは、有効な動画ファイルを/api/v1/extract_audioエンドポイントにアップロードした際に、
    レスポンスが200ステータスコード、zipファイル用の適切なヘッダー、および期待されるコンテンツを含むことを検証します。

    また、依存関係であるAudioExtractorとArchiverをモック化して、
    テストが外部依存に影響されないようにしています。
    """
    # 依存関係をモック化
    mock_extractor = AsyncMock()
    mock_extractor.extract_all_audio.return_value = ["audio1.mp3", "audio2.mp3"]

    mock_archiver = Mock()
    mock_archiver.create_archive.return_value = b"dummy zip content"

    # 依存関係をオーバーライド
    app.dependency_overrides[get_audio_extractor] = lambda: mock_extractor
    app.dependency_overrides[get_archiver] = lambda: mock_archiver

    try:
        response = client.post(
            "/api/v1/extract_audio",
            files={"file": ("valid_video.mp4", b"dummy video content", "video/mp4")}
        )

        assert response.status_code == 200
        assert response.headers["Content-Disposition"].startswith("attachment; filename=")
        assert response.headers["Content-Type"] == "application/zip"
    finally:
        # テスト後にオーバーライドをリセット
        app.dependency_overrides.clear()

def test_root_endpoint():
    """
    ルートエンドポイントのテスト。

    このテストは、ルートエンドポイントにアクセスした際に404ステータスコードが返されることを確認します。
    """
    response = client.get("/")
    assert response.status_code == 404

def test_extract_audio_invalid_file_type():
    """
    無効なファイルタイプでextract_audioエンドポイントをテスト。

    このテストは、非動画ファイル（例: テキストファイル）を/api/v1/extract_audioエンドポイントにアップロードした際に、
    400ステータスコードと適切なエラーメッセージが返されることを検証します。
    """
    response = client.post(
        "/api/v1/extract_audio",
        files={"file": ("test.txt", b"dummy content", "text/plain")}
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid file type: the uploaded file must be a video."

def test_extract_audio_empty_file():
    """
    空のファイルでextract_audioエンドポイントをテスト。

    このテストは、空の動画ファイルを/api/v1/extract_audioエンドポイントにアップロードした際に、
    500ステータスコードと適切なエラーメッセージが返されることを検証します。
    """
    response = client.post(
        "/api/v1/extract_audio",
        files={"file": ("empty.mp4", b"", "video/mp4")}
    )

    assert response.status_code == 500
    assert response.json()["message"] == "Audio extraction failed"
