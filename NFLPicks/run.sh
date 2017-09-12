#!binsh
echo "------ Starting APP ------"

if [-z $VCAP_APP_PORT];
	then SERVER_PORT=5000;
	else SERVER_PORT=$VCAP_APP_PORT;
fi

echo ------ Make database tables ------
python manage.py makemigrations
echo ------ Migrate database tables ------
python manage.py migrate --noinput

echo ------ Populating database tables ------
python manage.py loaddata db-backup.json

python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload