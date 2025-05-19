
# usage
# --------

# python manage.py generate_series_and_draw_graphs

from django.core.management.base import BaseCommand

# from pm_lookup.processing.scheduled_processing_2 import generate_series_and_draw_graphs
from pm_lookup.models import SerieParametersSet

"""
This command is to recreate the time series 
getting data from the  history data model.
It also recreates the graphs.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        #arrangia le serie storiche attingendo al modello storico grezzo e ridisegna i grafici

        serie_parameters_set_model = SerieParametersSet()

        serie_parameters_set_model.generate_series_and_draw_graphs()
