####################################################################################################
# マルチステージビルドで環境を分離
####################################################################################################
FROM node:24-bookworm AS base

# 作業ディレクトリを作成
RUN mkdir /app
WORKDIR /app

# 作業ユーザーを作成
ARG USER_ID
ARG GROUP_ID
RUN getent group $GROUP_ID && groupdel $(getent group $GROUP_ID | cut -d: -f1) || true && \
    getent passwd $USER_ID && userdel -r $(getent passwd $USER_ID | cut -d: -f1) || true && \
    groupadd -g $GROUP_ID appuser && \
    useradd -m -u $USER_ID -g appuser appuser

####################################################################################################
# 本番環境
####################################################################################################
FROM base AS production

# 無限にスリープ
USER appuser
CMD ["sleep", "infinity"]

####################################################################################################
# 開発環境
####################################################################################################
FROM base AS development

# 無限にスリープ
USER appuser
CMD ["sh", "-c", "npm install && sleep infinity"]