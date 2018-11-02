FROM python:alpine3.7

COPY . /code
WORKDIR /code

RUN apk update \
	&& apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl\
    && apk add mariadb-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev\
    g++ bash \
    && pip3 install wheel -r requirements.txt \
    && rm -rf /var/cache/apk/*
