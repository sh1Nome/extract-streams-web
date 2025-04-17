FROM python:3-slim

ARG ENV=production

RUN apt update \
    && apt install -y ffmpeg=7:5.1.6-0+deb12u1

RUN groupadd work \
    && useradd -g work work \
    && echo "work:password" | chpasswd

USER work

WORKDIR /home/work

COPY ./requirements.txt ./
COPY ./requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN if [ "$ENV" = "development" ]; then pip install --no-cache-dir -r requirements-dev.txt; fi
