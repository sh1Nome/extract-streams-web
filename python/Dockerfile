####################################################################################################
# マルチステージビルドで環境を分離
####################################################################################################
FROM python:3-slim AS base

# 作業ディレクトリを作成
RUN mkdir /app
WORKDIR /app

# 作業ユーザーを作成
ARG USER_ID
ARG GROUP_ID
RUN getent group $GROUP_ID && groupdel $(getent group $GROUP_ID | cut -d: -f1) || true && \
    getent passwd $USER_ID && userdel -r $(getent passwd $USER_ID | cut -d: -f1) || true && \
    groupadd -g $GROUP_ID appuser && \
    useradd -m -u $USER_ID -g appuser appuser && \
    chown appuser:appuser /app

# 依存解決
RUN apt update && apt install -y ffmpeg
COPY ./requirements.txt ./

####################################################################################################
# 本番環境
####################################################################################################
FROM base AS production

# 依存解決
RUN pip install --no-cache-dir -r requirements.txt

# サーバーの起動
USER appuser
CMD ["sh", "run_server.sh"]

####################################################################################################
# 開発環境
####################################################################################################
FROM base AS development

# 依存解決
COPY ./requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r requirements-dev.txt

# CMD命令でテストを実行し、無限にスリープ
USER appuser
CMD [ "sh", "-c", "rm -f /tmp/healthcheck_passed /tmp/healthcheck_failed && \
    sh ./tests/run_tests.sh && \
    touch /tmp/healthcheck_passed || \
    touch /tmp/healthcheck_failed; \
    sleep infinity" ]

# HEALTHCHECKでテスト結果を確認
HEALTHCHECK --interval=5s \
            --timeout=3s \
            --start-period=5s \
            --retries=20 \
            CMD [ "sh", "-c", "test -f /tmp/healthcheck_passed && exit 0 || exit 1" ]
