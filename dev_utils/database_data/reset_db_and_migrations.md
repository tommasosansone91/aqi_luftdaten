# reset_db_and_migrations

## hard fix migration issues by recreating model as if it were the first time in the app history

>[!CAUTION]
> migrations must **never** be gitignored.

create models as you were doing it for the first time in the app history:

delete the tables and the history of migrations in the database: drop the database:

-     psql -h localhost -U postgres -d postgres

-     drop database aqi_graphs_dashboard;

recreate a fresh database:

-     create database aqi_graphs_dashboard;

-     alter database aqi_graphs_dashboard OWNER TO aqigd_main;

-     exit

-     psql -h localhost -U aqigd_main -d aqi_graphs_dashboard

delete the history of migrations on the migration folder

- delete all files inside folder migrations, except `__init__.py`

create models (this is as you were doing it for the first time in the app history):

-     source venv/bin/activate

-     python manage.py makemigrations

-     python manage.py migrate

align the project models to the remote project models:

-     git restore pm_lookup/migrations/

discard the history of migrations tracked in the database: drop the database:

-     psql -h localhost -U postgres -d postgres

-     drop database aqi_graphs_dashboard;

-     create database aqi_graphs_dashboard;

-     alter database aqi_graphs_dashboard OWNER TO aqigd_main;

-     exit

-     psql -h localhost -U aqigd_main -d aqi_graphs_dashboard

run the makemigration command, just to verify that it will have no effect

-     source venv/bin/activate

-     python manage.py makemigrations

generate the tables in the db: run the migration command

-     python manage.py migrate

recreate the superuser 

-     python manage.py createsuperuser


## git strategy for migrations

>[!IMPORTANT]
> The folder must be aligned across all the developing machines.

Every time a developer work on the model, it should 

- git pull the migrations, 

- apply them via makemigrations, migrate, 

- apply the new migrations via makemigrations, migrate

- commit and push the migrations.


-----------

## useful commands

access the db

    psql -h localhost -U aqigd_main -d aqi_graphs_dashboard


show all tables

    \dt


-------------
