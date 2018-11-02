FROM python:alpine3.7

COPY . /code
WORKDIR /code

RUN apk update \
    && apk add mariadb-dev \
    g++ bash \
    && pip3 install wheel -r requirements.txt \
    && rm -rf /var/cache/apk/*

# for Pillow
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev