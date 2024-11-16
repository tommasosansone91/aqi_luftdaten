from django.core.management.base import BaseCommand
from pm_lookup.models import realtime_datapoints

"""
This command is to delete all data in the realtime model.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        realtime_datapoints.objects.all().delete()
