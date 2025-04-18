
import numpy as np 
import math

import time
from datetime import datetime

import json
import requests

from pm_lookup.config import ALL_SENSORS_DATA_URL, KILOMETERS_TO_COORDINATES_POINTS_DISTANCE
from pm_lookup.models import TargetArea

from .air_quality_evaluators import evaluate_PM10, evaluate_PM25

# per conversione della timezone e check ora legale
from .time_converters import convert_datetime_timezone, add_one_hour


def extract_data_from_sensors_network_for_all_places():

    # url generating
    api_URL = ALL_SENSORS_DATA_URL

    print("In attesa di ricevere i dati...")

    # go grab the api
    api_request = requests.get(api_URL)

    # save time
    # record_time = datetime.now()
    #  l'ho definito dopo

    print("Dati ricevuti!")

    # record parse
    try:
        # json parsa il contenuto di api_request in 
        api_response_data = json.loads(api_request.content)

    except json.JSONDecodeError as e:
        api_response_data = []
        print("Errore: il contenuto della response non è un JSON valido. \n{}".format(e))

    # prende dati input
    input_data = TargetArea.objects.all()

    # dai dati acquisiti, individua quelli che corrispondono al perimetro delle località selezionate, 
    # e salvane i valori

    processed_data_for_all_places = list()


    for place in input_data:

        place_id = place.id
        
        place_name = place.name

        print("Inizio ricerca dati per %s..." % place_name)

        # predo lat e long e raggio della località input
        x_p = float(place.longitude)
        y_p = float(place.latitude)
        rho = KILOMETERS_TO_COORDINATES_POINTS_DISTANCE * float(place.radius) # fattore di trasformazione (coord/km)

        PM10_list = []
        PM25_list = []
        timestamp_list = []
    
        for sensor in api_response_data:

            got_PM_value = 0
            invalid_coordinates = 0

            try:
                x_s = float(sensor["location"]["longitude"])
            except:
                x_s = -9999
                invalid_coordinates = 1
                print("Longitudine invalida per il sensore in esame!")

            try:
                y_s = float(sensor["location"]["latitude"])
            except:
                y_s = -9999
                invalid_coordinates = 1
                print("Latitudine invalida per il sensore in esame!")

            
            # print("Latitudine e longitudine del sensore in esame: %s, %s" % (y_s, x_s) )
                        
            # termine 1 della formula

            t1 = math.sqrt( ( x_s - x_p )**2 + ( y_s - y_p )**2 )

            # termine 2 è rho

            if t1 <= rho and invalid_coordinates==0:

                

                # no perchè latitudine longitudine e rho non hanno la stessa unità di misura
                # ho convertito il raggio in lat e logn-- 8km ~~ 0.043702 .... per milano



                print("Trovato un sensore entro l'area definita per %s:" % place_name)
                print("    Latitudine e longitudine: %s, %s" % (y_s, x_s) )

                # allora estrai  le info del pm 



                for physical_quantity_recorded in sensor['sensordatavalues']:

                    if physical_quantity_recorded['value_type'] == 'P1':

                        PM10_value = physical_quantity_recorded['value']               
                        PM10_list.append(PM10_value)
                        got_PM_value = 1
                        print("    PM10: %s" % PM10_value)

                    if physical_quantity_recorded['value_type'] == 'P2':

                        PM25_value = physical_quantity_recorded['value']                
                        PM25_list.append(PM25_value)
                        got_PM_value = 1
                        print("    PM2.5: %s" % PM25_value)

                # fuori dal loop delle grandezze fisiche, c'è un solo timestamp per ogni centralina
                if got_PM_value==1:
                    
                    timestamp_value = sensor['timestamp']

                    # correzione del timestamp da una zona ad un'altra 
                    timestamp_value = convert_datetime_timezone(timestamp_value, "Europe/London", "Europe/Berlin")
                    
                    # e sposta avanti la lancetta di uno se è attiva l'ora legale. infatti il server di luftdaten non ne tiene conto.
                    
                    # se è attiva l'ora legale nel tempo locale
                    if time.localtime().tm_isdst != 0:
                        # sposta le lancette avanti di uno
                        timestamp_value = add_one_hour(timestamp_value)

                    timestamp_list.append(timestamp_value)  
                    print("    Timestamp: %s" % timestamp_value)                 

                else:
                    print("    Questo sensore non possiede dati di particolato")    

            # end processing for one sensonr

        # end processing for all sensors

        # aggregating arrays of data

        # da qui in poi il  processing è lo stesso per diversi metodi di raccota dati

        number_of_contributing_sensors = max ( len(PM10_list), len(PM25_list) )

        if number_of_contributing_sensors == 0:
            print("Nell'area selezionata per %s non ci sono sensori, oppure non sono reperibili!" % place_name)
            print("---------------------------------------------------")
            continue


        number_of_contributing_sensors = len(PM10_list)
        
        PM10_array = np.array(PM10_list)
        PM10_array = PM10_array.astype(float)

        PM25_array = np.array(PM25_list)
        PM25_array = PM25_array.astype(float)

        timestamp_array = np.array(timestamp_list)

        PM10_mean = round(np.mean(PM10_array), 2)
        PM25_mean = round(np.mean(PM25_array), 2)

        # col min prendo il tempo del sensore aggiornato meno di recente, per garanzia di aggiornamento minimo
        oldest_record_time_among_sensors_for_one_place = min(timestamp_array)
        # max_record_time_among_sensors_for_one_place = max(timestamp_array)
        
        # da solo non è necessario
        oldest_record_time_among_sensors_for_one_place = datetime.strptime(oldest_record_time_among_sensors_for_one_place, "%Y-%m-%d %H:%M:%S")

        # oldest_record_time_among_sensors_for_one_place = oldest_record_time_among_sensors_for_one_place.strftime("%d-%m-%Y %H:%M:%S")
        #  se lo metto dice che deve essere formattato in formato che mantega anche la timezone

        # passo in entrata un valore del pm e mi viene restituito in uscita il messaggio e la classe css corrispondente
        [PM10_mean_cathegory_label, PM10_mean_cathegory] = evaluate_PM10(PM10_mean)

        [PM25_mean_cathegory_label, PM25_mean_cathegory] = evaluate_PM25(PM25_mean)
            


# return a list of objects containing the info that can be saved or not in the fileds of the model that we want to ave the retrieved data into
# # also pass this
# common_output = {
#         'api_URL':api_URL, 
#         'api_response_data':api_response_data,             
#         }

        processed_data_from_detected_sensors_for_one_place = {

            "target_area_id": place_id,
            # all'inizio del ciclo savlo la id dell'oggetto che sto scorrendo
            # quindi qui dico: salva i dati nel campo foreign key 
            # che rimanda all'oggetto avente per id quello che mi sono salvato
                                                    
            "last_update_time": oldest_record_time_among_sensors_for_one_place,

            "PM10_mean":PM10_mean,
            "PM25_mean":PM25_mean,

            "PM10_mean_cathegory_label":PM10_mean_cathegory_label,
            "PM25_mean_cathegory_label":PM25_mean_cathegory_label,
            "PM10_mean_cathegory": PM10_mean_cathegory,
            "PM25_mean_cathegory": PM25_mean_cathegory,

            "number_of_contributing_sensors": number_of_contributing_sensors
        }


        processed_data_for_all_places.append( processed_data_from_detected_sensors_for_one_place )

        print("Valori del particolato raccolti da %s sensori per %s:" % (number_of_contributing_sensors, place_name))

        print("PM10:")
        print(PM10_list)  

        print("PM2.5:")
        print(PM25_list)  

        print("Orari delle rilevazioni:")
        print(timestamp_list) 

        print("Valore medio del PM10 per %s: %s µg/m³. %s" % (place_name, PM10_mean, PM10_mean_cathegory_label))
        print("Valore medio del PM2.5 per %s: %s µg/m³. %s" % (place_name, PM25_mean, PM25_mean_cathegory_label))
        print("Timestamp delle osservazioni per %s: %s" % (place_name, oldest_record_time_among_sensors_for_one_place))

        # end the processing for one place


    api_data = {
            'api_URL': api_URL, 
            'api_response_data': api_response_data,
            }
    

    results_dict = {
        "api_data": api_data,
        "processed_data_for_all_places": processed_data_for_all_places
    }

    # end the processing for all places
    
    return results_dict