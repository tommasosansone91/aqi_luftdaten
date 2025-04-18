# reset_db_and_migrations


source venv/bin/activate

psql -h localhost -U postgres -d postgres

drop database aqiluftdaten;

create database aqiluftdaten;

alter database aqiluftdaten OWNER TO luftdaten_main;

psql -h localhost -U luftdaten_main -d aqiluftdaten

python manage.py migrate

python manage.py createsuperuser



-----------

psql -h localhost -U luftdaten_main -d aqiluftdaten

\dt


-------------
