#!/bin/sh

# テストスクリプト: FastAPIアプリケーションのテストを実行

# 環境変数の設定
export PYTHONPATH=~/apisource
PYTEST_EXECUTABLE=~/.local/bin/pytest

if [ ! -x "$PYTEST_EXECUTABLE" ]; then
    echo "pytestが見つかりません。インストールされていることを確認してください。"
    exit 1
fi

# pytestを使用してテストを実行
echo "pytestでテストを実行中..."
$PYTEST_EXECUTABLE --cache-clear

# テスト結果の終了ステータスを取得
TEST_STATUS=$?

if [ $TEST_STATUS -eq 0 ]; then
    echo "すべてのテストが正常にパスしました。"
else
    echo "いくつかのテストが失敗しました。詳細は上記の出力を確認してください。"
fi

exit $TEST_STATUS