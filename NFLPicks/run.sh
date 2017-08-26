#!binsh
echo "------ Starting APP ------"
USER="admin"
MAIL="admin@gmail.com"
PASS="secret06"

if [-z $VCAP_APP_PORT];
	then SERVER_PORT=5000;
	else SERVER_PORT=$VCAP_APP_PORT;
fi

echo ------ Make database tables ------
python manage.py makemigrations
echo ------ Migrate database tables ------
python manage.py migrate --noinput

echo "from django.contrib.auth.models import User; User.objects.create_superuser('${USER}', '${MAIL}', '${PASS}')" | python manage.py shell

python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload