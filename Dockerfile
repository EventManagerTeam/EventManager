FROM python:alpine3.7

COPY . /code
WORKDIR /code

RUN apk update \
    && apk add mariadb-dev \
    g++ bash \
    && pip3 install wheel -r requirements.txt \
    && rm -rf /var/cache/apk/*