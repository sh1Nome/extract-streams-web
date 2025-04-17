"""
このモジュールは、FastAPIアプリケーションのテストケースを含んでいます。
FastAPIのTestClientを使用してリクエストをシミュレートし、レスポンスを検証します。

テストケース:
- test_root_endpoint: ルートエンドポイントが404ステータスコードを返すことを確認します。
- test_extract_audio_invalid_file_type: 無効なファイルタイプをアップロードした場合に、400ステータスコードと適切なエラーメッセージが返されることを検証します。
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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