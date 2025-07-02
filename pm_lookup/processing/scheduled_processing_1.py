

from pm_lookup.models import AreaParametersSet
from pm_lookup.models import HistoricalDatapoint

from pm_lookup.processing.utils.sensors_network_data_processing import extract_data_from_sensors_network_for_all_places


def get_data_from_luftdaten_api_and_save_them_in_HistoricalDatapoint():    

    sensors_network_data = extract_data_from_sensors_network_for_all_places()

    print(sensors_network_data["processed_data_for_all_places"])

    for place in sensors_network_data["processed_data_for_all_places"]:

        try:

            area_parameters_set_object = AreaParametersSet.objects.get(
                    id=place["area_parameters_set"].id
                )

            new_historical_record = HistoricalDatapoint(
                
                area_parameters_set = area_parameters_set_object,

                last_update_time = place["last_update_time"],

                PM10_mean = place["PM10_mean"],
                PM25_mean = place["PM25_mean"],

                number_of_contributing_sensors = place["number_of_contributing_sensors"],
            )
            
            new_historical_record.save()

            print("Dati per %s salvati nel modello storico!" % area_parameters_set_object.name)

        except Exception as e:
            print(e)
            # print("Vincolo unique together violato: i dati acquisiti sono uguali ai precedenti.")
            print("Viene impedita l'aggiunta del record [area di interesse: %s Timestamp: %s PM10: %s PM2.5: %s] al modello storico .".format(
                area_parameters_set_object,  # using the object string representation of TargetAarea
                place["last_update_time"], 
                place["PM10_mean"], 
                place["PM25_mean"]
                )
            )

            print("I dati acquisiti non sono stati salvati.")

        print("---------------------------------------------------")


    # quando ha processato tutti i posti
    print("I nuovi dati per tutte le aree di interesse sono stati salvati nel modello storico!")

    print("---------------------------------------------------")




    # non ritorna niente perchè deve solo alvare in history



