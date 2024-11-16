from django.core.management.base import BaseCommand
from pm_lookup.models import RealtimeDatapoints

"""
This command is to delete all data in the realtime model.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        RealtimeDatapoints.objects.all().delete()
