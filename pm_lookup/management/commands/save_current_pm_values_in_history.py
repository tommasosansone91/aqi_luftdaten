from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing import save_history_pm
from pm_lookup.processing.scheduled_processing_2 import arrange_time_series_and_graphs


# quando scrivo
# python manage.py save_current_pm_values_in_history
# la funzione command viene rannata automaticamente

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #salva i valori nel modello storico grezzo
        save_history_pm()
        

