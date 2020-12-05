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



echo "Clearing out old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete


echo "Apply database migrations...."
python manage.py makemigrations
python manage.py makemigrations parent
python manage.py migrate

echo "Setting superuser"

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')"


exec "$@"
