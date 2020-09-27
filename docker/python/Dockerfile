FROM python:3.7-alpine

RUN apk update \
    && apk add --no-cache --virtual bash \
    && apk add gcc \
    && apk add musl-dev \
    && apk add linux-headers \
    && apk add jpeg-dev \
    && apk add zlib-dev \
    && apk add mariadb-dev \
    && apk add libffi-dev \
    && apk add g++

# install pypi packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm /usr/bin/mysql*
COPY uwsgi.ini /uwsgi.ini

CMD ["uwsgi", "--ini", "/uwsgi.ini"]


# copy entrypoint.sh
COPY ./entrypoint.sh /entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN apk add --no-cache bash coreutils grep sed
