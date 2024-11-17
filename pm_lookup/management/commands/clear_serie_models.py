
# usage
#----------

# python manage.py clear_models


from django.core.management.base import BaseCommand
from pm_lookup.models import \
    RealtimeDatapoints, \
    DatapointsSerieComputed

"""
This command is to delete all data in the series models.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        # RealtimeDatapoints.objects.all().delete()

        # deleting the series(+graphs), not the historical dataponts
        DatapointsSerieParameters.objects.all().delete()
        DatapointsSerieComputed.objects.all().delete()
