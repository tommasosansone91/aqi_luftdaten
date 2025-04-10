from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing import save_history_pm
from pm_lookup.processing.scheduled_processing_2 import arrange_time_series_and_graphs
from pm_lookup.processing.scheduled_processing_3 import arrange_daily_time_series_and_graphs

# this is to fill the db with current pm values and arrange daily and pluridaily series

# quando scrivo
# python manage.py devmode_fill_db_with_current_pm_values_and_arrange_series
# la funzione command viene rannata automaticamente

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #salva i valori nel modello storico grezzo
        save_history_pm()

        #arrangia le serie storiche orarie attingendo al modello storico grezzo e ridisegna i grafici
        arrange_time_series_and_graphs()

        #arrangia le serie storiche giornaliere attingendo al modello storico grezzo e ridisegna i grafici
        arrange_daily_time_series_and_graphs()


        

