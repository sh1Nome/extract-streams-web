#!/bin/bash

# .envファイルのパス
env_file=".env"

# .env_defaultファイルのパス
default_env_file=".env_default"

# 現在のUSER_IDとGROUP_IDを取得
user_id=$(id -u)
group_id=$(id -g)

# .envファイルを生成または更新
if [ -f "$default_env_file" ]; then
  cp "$default_env_file" "$env_file"
  sed -i "s/^USER_ID=.*/USER_ID=$user_id/" "$env_file"
  sed -i "s/^GROUP_ID=.*/GROUP_ID=$group_id/" "$env_file"
  echo ".envファイルを生成または更新しました: USER_ID=$user_id, GROUP_ID=$group_id"
else
  echo "$default_env_fileが見つかりません。"
  exit 1
fi