# creo uno script per poterlo usare nell'heroku scheduler
# ne faccio un base command, così ogni tot heroku lo ranna ed è come se lo runnasse da consolle


from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing import save_history_pm
from pm_lookup.processing.scheduled_processing_2 import arrange_time_series_and_graphs
from pm_lookup.processing.scheduled_processing_3 import arrange_daily_time_series_and_graphs

# quando scrivo
# python manage.py save_current_pm_values_in_history
# la funzione command viene rannata automaticamente

class Command(BaseCommand):
    def handle(self, *args, **options):

        save_history_pm()
        
        arrange_time_series_and_graphs()
        arrange_daily_time_series_and_graphs()