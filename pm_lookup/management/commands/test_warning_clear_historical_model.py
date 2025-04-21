
# usage
#----------

# python manage.py test_warning_clear_historical_model


from django.core.management.base import BaseCommand
from pm_lookup.models import HistoricalDatapoints

"""
This command is to delete all data in the historical model.

IT SHOULD NEVER BE RUN IN PRODUCTION
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        user_input = input("You are going to DELETE ALL DATA IN THE HISTORICAL DATA MODEL\nAre you sure? Type 'yes' to continue: ")

        if user_input.lower() != "yes":
            print("Exiting script.")
            exit()

        print("You typed 'yes'. Continuing...")

        # deleting the historical datapoints
        HistoricalDatapoints.objects.all().delete()

