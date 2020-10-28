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

#ENV DJANGO_DB_NAME=django
#ENV DJANGO_SU_NAME=admin
#ENV DJANGO_SU_EMAIL=kiddy.up.help@gmail.com
#ENV DJANGO_SU_PASSWORD=password


#RUN python -c "import django; django.setup(); \
#   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
#   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
#   username='$DJANGO_SU_NAME', \
#   email='$DJANGO_SU_EMAIL', \
#   password='$DJANGO_SU_PASSWORD')"

