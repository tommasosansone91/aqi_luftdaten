
# usage
#----------

# python manage.py clear_models


from django.core.management.base import BaseCommand
from pm_lookup.models import \
    RealtimeDatapoints, \
    DatapointsSerie, \
    DailyAggregatedDatapointsSerie, \
    HourlyAggregatedDatapointsSerie

"""
This command is to delete all data in the series models.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        # RealtimeDatapoints.objects.all().delete()

        DatapointsSerie.objects.all().delete()
        DailyAggregatedDatapointsSerie.objects.all().delete()
        HourlyAggregatedDatapointsSerie.objects.all().delete()