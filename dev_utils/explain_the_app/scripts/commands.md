# commands

> pm_lookup/management/commands

these scrips can be run by

    cd /var/www/aqi_graphs_dashboard
    source venv/bin/activate
    venv/bin/python manage.py <script_name>

e.g.

to run 

> pm_lookup/management/commands/get_data_from_sensorcommunity_api_and_save_them_in_history.py

    python manage.py get_data_from_sensorcommunity_api_and_save_them_in_history


### get_data_from_sensorcommunity_api_and_save_them_in_history

chiama la API Sensor Community per ottenere e salvare i dati nel modello storico grezzo

    get_current_pm_values_and_save_them_in_history()



