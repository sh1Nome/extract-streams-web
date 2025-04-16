#!/bin/sh

# 翻訳ファイルを更新するスクリプトを実行
sh /home/work/apisource/translations/update_translations.sh

# Uvicornサーバーを起動
../.local/bin/uvicorn main:app --host 0.0.0.0