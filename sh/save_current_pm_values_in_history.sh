#!/bin/bash

cd /var/www/aqi_luftdaten

# source venv/bin/activate

venv/bin/python manage.py save_current_pm_values_in_history
