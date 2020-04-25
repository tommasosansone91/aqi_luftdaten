from django.core.management.base import BaseCommand
from pm_lookup.models import target_area_output_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        target_area_output_data.objects.all().delete()
