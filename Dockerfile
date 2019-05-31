FROM python:alpine3.7

# for Pillow
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc libressl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN apk update \
    && apk add mariadb-dev \
    g++ bash \
    && rm -rf /var/cache/apk/*

COPY . /code
WORKDIR /code

RUN pip3 install wheel -r requirements.txt
