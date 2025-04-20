#!/bin/bash

# testsディレクトリ内のPythonファイルのdocstringをHTMLに変換するスクリプト

# 出力ディレクトリ
OUTPUT_DIR="docstrings_html"
mkdir -p "$OUTPUT_DIR"

# PYTHONPATHをルートディレクトリに設定
export PYTHONPATH=$(pwd)/..

# ベースモジュール名
BASE_MODULE="tests"

# testsディレクトリ内のPythonファイルを検索して処理
for file in $(find . -name "*.py" -type f); do
    # ファイル名から拡張子を除いた名前を取得
    base_name="$(basename "$file" .py)"
    
    # pydocコマンドを使用してHTMLに変換
    pydoc -w "$BASE_MODULE.$base_name"
    
    # 出力ファイルを指定ディレクトリに移動
    if [ -f "$BASE_MODULE.${base_name}.html" ]; then
        mv "$BASE_MODULE.${base_name}.html" "$OUTPUT_DIR/${base_name}.html"
    else
        echo "Error: $BASE_MODULE.${base_name}.html not found. Skipping."
    fi
done

echo "$BASE_MODULEディレクトリ内のPythonファイルのdocstringがHTMLに変換されました。出力先: $OUTPUT_DIR"