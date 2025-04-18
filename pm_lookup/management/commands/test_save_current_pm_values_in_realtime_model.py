
from django.core.management.base import BaseCommand

from pm_lookup.processing.realtime_processing_1 import get_current_pm_values_and_save_them_in_RealtimeDatapoints

from django.db import IntegrityError

"""this is just for development/test"""


# usage
#----------

# python manage.py test_save_current_pm_values_in_realtime_model


# questo file lo richiamo solo se c'e l'ho in 
# app/management/commands/nome_file.py
# la linea from django.core.management.base import BaseCommand
# l'intestazione
# class Command(BaseCommand):
#     def handle(self, *args, **options):


class Command(BaseCommand):
    def handle(self, *args, **options):

        get_current_pm_values_and_save_them_in_RealtimeDatapoints()