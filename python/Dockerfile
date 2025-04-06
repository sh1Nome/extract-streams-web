FROM python:3-slim

RUN groupadd work \
    && useradd -g work work \
    && echo "work:password" | chpasswd

USER work

WORKDIR /home/work

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
