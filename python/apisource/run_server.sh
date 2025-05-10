#!/bin/sh

# 翻訳ファイルを更新するスクリプトを実行
sh /app/translations/update_translations.sh

# Uvicornサーバーを起動
uvicorn main:app --host 0.0.0.0