
from pm_lookup.models import TargetArea
from pm_lookup.models import RealtimeDatapoints

from pm_lookup.processing.utils.sensors_network_data_processing import extract_data_from_sensors_network_for_all_places


def get_current_pm_values_and_save_them_in_RealtimeDatapoints():    

    # nel modello realtime voglio un solo oggetto per area
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

            object_place = TargetArea.objects.get(
                    id=place["target_area_id"]
                    )

            object_place_name = object_place.name

            print("Dati per %s salvati nel modello realtime!" % object_place)
            # using the object string representation of TargetAarea

            print("---------------------------------------------------")


        except Exception as e:
            print("Errore nel salvataggio dei dati realtime. \n{}".format(e))

    # quando ha processato tutti i posti
    print("---------------------------------------------------")