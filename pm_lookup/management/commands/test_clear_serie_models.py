
# usage
#----------

# python manage.py clear_models


from django.core.management.base import BaseCommand
from pm_lookup.models import \
    SerieParametersSet, \
    ComputedSerie

"""
This command is to delete all data in the series models.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        # RealtimeDatapoints.objects.all().delete()

        # deleting the series(+graphs), not the historical dataponts
        SerieParametersSet.objects.all().delete()
        ComputedSerie.objects.all().delete()
