from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_2 import arrange_time_series_and_graphs

# quando scrivo
# python manage.py predispose_historical_series
# la funzione command viene rannata automaticamente
class Command(BaseCommand):
    def handle(self, *args, **options):

        arrange_time_series_and_graphs()