FROM python:3-slim

RUN apt update \
    && apt install -y ffmpeg=7:5.1.6-0+deb12u1

RUN groupadd work \
    && useradd -g work work \
    && echo "work:password" | chpasswd

USER work

WORKDIR /home/work

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
