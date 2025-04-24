# マルチステージビルドで環境を分離
FROM python:3-slim AS base

RUN apt update && apt install -y ffmpeg=7:5.1.6-0+deb12u1

RUN groupadd work && useradd -g work work && echo "work:password" | chpasswd

USER work
WORKDIR /home/work

COPY ./requirements.txt ./

# 本番環境
FROM base AS production

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "run_server.sh"]

# 開発環境
FROM base AS development

COPY ./requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r requirements-dev.txt

# CMD命令でテストを実行し、無限にスリープ
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

