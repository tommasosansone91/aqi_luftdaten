
# usage
#----------

# python manage.py save_current_pm_values_in_history_model


from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_1 import get_data_from_luftdaten_api_and_save_them_in_HistoricalDatapoint

"""
This command is to get the data from luftdaten api and save them in hsitorical model.
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #salva i valori nel modello storico grezzo
        get_data_from_luftdaten_api_and_save_them_in_HistoricalDatapoint()

        

