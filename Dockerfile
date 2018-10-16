FROM python:alpine3.7

ENV PIP_CACHE_DIR .cache

COPY . /code
WORKDIR /code

RUN apk update \
    && apk add mariadb-dev \
    g++ bash \
    && pip3 install wheel -r requirements.txt --target cached-dependencies \
    && cp -rp cached-dependencies/* /usr/local/lib/python3.6/site-packages/ \
    && rm -rf cached-dependencies \
    && rm -rf /var/cache/apk/*
