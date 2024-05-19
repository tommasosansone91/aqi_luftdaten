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

    save_history_pm()


### arrange_historical_and_daily_series

arrangia/disegna le serie *orarie* e *giornaliere* attingendo al modello storico grezzo

    arrange_daily_time_series_and_graphs()

**NOTA**: è necessario lanciare questo script quando un grande ammontare di dati recenti vengono rimossi dal modello storico grezzo.


### arrange_daily_series

arrangia/disegna le serie *giornaliere* attingendo al modello storico grezzo

    arrange_daily_time_series_and_graphs()

**NOTA**: è necessario lanciare questo script quando un grande ammontare di dati recenti vengono rimossi dal modello storico grezzo.


### clear_models

cancella tutti i dati nei modelli dei dati storici

