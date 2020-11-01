#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MySQL started"
fi
#
#DJANGO_DB_NAME=django
#DJANGO_SU_NAME=admin
#DJANGO_SU_EMAIL=kiddy.up.help@gmail.com
#DJANGO_SU_PASSWORD=password






#python manage.py flush --no-input
python manage.py makemigrations
#python manage.py makemigrations parent
#python manage.py migrate --fake parent zero
#python manage.py migrate parent
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')"


exec "$@"
