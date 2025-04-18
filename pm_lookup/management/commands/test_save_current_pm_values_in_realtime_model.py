
from django.core.management.base import BaseCommand

from pm_lookup.models import TargetArea, RealtimeDatapoints

from pm_lookup.processing.utils.sensors_network_data_processing import extract_data_from_sensors_network_for_all_places

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

        RealtimeDatapoints.objects.all().delete()

        sensors_network_data = extract_data_from_sensors_network_for_all_places()

        print(sensors_network_data["processed_data_for_all_places"])

        for place in sensors_network_data["processed_data_for_all_places"]:

            try:

                new_realtime_record = RealtimeDatapoints(
                    
                    target_area = TargetArea.objects.get(
                        id=place["target_area_id"]
                        ),

                    last_update_time = place["last_update_time"],

                    PM10_mean = place["PM10_mean"],
                    PM25_mean = place["PM25_mean"],

                    PM10_mean_cathegory_label = place["PM10_mean_cathegory_label"],
                    PM25_mean_cathegory_label = place["PM25_mean_cathegory_label"],
                    PM10_mean_cathegory = place["PM10_mean_cathegory"],
                    PM25_mean_cathegory = place["PM25_mean_cathegory"],

                    number_of_contributing_sensors = place["number_of_contributing_sensors"],
                )
                
                new_realtime_record.save()

            except Exception as e:
                print("Errore di integrità: {}".format(e))

        # quando ha processato tutti i posti

        


