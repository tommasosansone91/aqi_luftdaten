
# usage
# --------

# python manage.py generate_series_and_draw_graphs

from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_2 import generate_series_and_draw_graphs

"""
This command is to recreate the time series 
getting data from the  history data model.
It also recreates the graphs.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        #arrangia le serie storiche orarie attingendo al modello storico grezzo e ridisegna i grafici
        generate_series_and_draw_graphs()
