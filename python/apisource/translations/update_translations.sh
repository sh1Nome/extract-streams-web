#!/bin/bash

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 新しいメッセージを抽出してmessages.potを更新
pybabel extract -F babel.cfg -o messages.pot ..

# 新しいメッセージで.poファイルを更新
pybabel update -i messages.pot -d .

# .poファイルをコンパイルして.moファイルを生成
pybabel compile -d .

# POT-Creation-Dateは翻訳テンプレートが生成された日時を示すメタデータです。
# この処理は、スクリプトを実行するたびにPOT-Creation-Dateの差分が出ないようにするためです。
# 具体的には、sedコマンドを使用して以下のファイルからPOT-Creation-Date行を削除することで、日時の変更による不要な差分を防いでいます。
# - messages.pot
# - 各言語ディレクトリ内のmessages.po (例: en/LC_MESSAGES/messages.po, ja/LC_MESSAGES/messages.po)
sed -i '/^"POT-Creation-Date:/d' messages.pot
find . -name "messages.po" -exec sed -i '/^"POT-Creation-Date:/d' {} +

echo "翻訳ファイルが正常に更新およびコンパイルされました。"
