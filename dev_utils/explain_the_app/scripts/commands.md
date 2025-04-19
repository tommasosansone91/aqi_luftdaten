# commands

> pm_lookup/management/commands

these scrips can be run by

    cd /var/www/aqi_luftdaten
    source venv/bin/activate
    venv/bin/python manage.py <script_name>

e.g.

to run 

> pm_lookup/management/commands/save_current_pm_values_in_history.py

    python manage.py save_current_pm_values_in_history


### save_current_pm_values_in_history

chiama la API Luftdaten per ottenere e salvare i dati nel modello storico grezzo

    get_current_pm_values_and_save_them_in_history()



