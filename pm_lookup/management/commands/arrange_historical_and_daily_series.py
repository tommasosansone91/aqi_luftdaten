from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_2 import arrange_time_series_and_graphs
from pm_lookup.processing.scheduled_processing_3 import arrange_daily_time_series_and_graphs

"""
This command is to recreate the hourly and daily time series 
getting data from the  history data model.
It also recreates the graphs.
"""

# con questo script verifico 
# se sono ok e funzioni che aggiornano le serie storiche e relativi grafici
# inoltre ridisegna i grafici delle serie orarie, giornaliere

# quando scrivo
# python manage.py arrange_historical_series
# la funzione command viene rannata automaticamente
class Command(BaseCommand):
    def handle(self, *args, **options):

        #arrangia le serie storiche orarie attingendo al modello storico grezzo e ridisegna i grafici
        arrange_time_series_and_graphs()

        #arrangia le serie storiche giornaliere attingendo al modello storico grezzo e ridisegna i grafici
        arrange_daily_time_series_and_graphs()