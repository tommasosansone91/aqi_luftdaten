#!/bin/bash

# this file will be triggered by the cron and launch the BaseCommand to store data into the database.

cd /var/www/aqi_luftdaten

# source venv/bin/activate
# it is not needed since I specify the python interpreter from the venv in the next line


venv/bin/python manage.py get_data_from_luftdaten_api_and_save_them_in_history


venv/bin/python manage.py generate_series_and_draw_graphs
