
# usage
#----------

# python manage.py save_current_pm_values_in_history


from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_1 import get_current_pm_values_and_save_them_in_history
from pm_lookup.processing.scheduled_processing_2 import arrange_datapoints_series_and_graphs


# quando scrivo
# python manage.py save_current_pm_values_in_history
# la funzione command viene rannata automaticamente

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #salva i valori nel modello storico grezzo
        get_current_pm_values_and_save_them_in_history()
        

