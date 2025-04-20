# reset_db_and_migrations

delete all files inside folder migrations, except `__init__.py`

    source venv/bin/activate

    psql -h localhost -U postgres -d postgres

    drop database aqiluftdaten;

    create database aqiluftdaten;

    alter database aqiluftdaten OWNER TO luftdaten_main;

    exit

    psql -h localhost -U luftdaten_main -d aqiluftdaten

    python manage.py migrate

    python manage.py makemigrations

    python manage.py createsuperuser



-----------

psql -h localhost -U luftdaten_main -d aqiluftdaten

\dt


-------------
