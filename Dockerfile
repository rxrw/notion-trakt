FROM python:3.10-alpine

LABEL maintainer="Jens Lee <rxrw@me.com>"
LABEL version="1.0.0"

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade setuptools \
    && pip install --no-cache-dir --upgrade wheel \
    && pip install --no-cache-dir --upgrade cryptography \
    && apk del .build-deps

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ADD . /app

ENTRYPOINT ["python", "main.py"]
