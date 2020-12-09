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

echo "Setting superuser..."

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')"

# ----------- BJD ------------------
echo "Creating Bethany's test users..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('803box', '803box@gmail.com', 'AllCats1!')"

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('bdeme004', 'bdeme004@odu.edu', 'AllCats1!')"

echo "Assigning children to test users..."
python manage.py shell -c "from django.core import management; from django.core.management.commands import loaddata;management.call_command('loaddata', 'thedata.json', verbosity=0)"

exec "$@"
