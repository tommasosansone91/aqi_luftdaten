from django.core.management.base import BaseCommand

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from pm_lookup.processing.scheduled_processing import save_history_pm

# quando scrivo
# python manage.py save_current_pm_values_in_history
# la funzione command viene rannata automaticamente

class Command(BaseCommand):
    def handle(self, *args, **options):

        save_history_pm()