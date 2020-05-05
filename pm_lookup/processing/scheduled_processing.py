
import numpy as np 
import math

import time
from datetime import datetime
from django.utils import timezone

import json
import requests

from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_output_data
from pm_lookup.models import target_area_history_data

from .auxiliary_processing import evaluate_PM10
from .auxiliary_processing import evaluate_PM25
from .auxiliary_processing import save_in_history


def get_realtime_pm():    

    
    # url generating
    api_URL = "https://data.sensor.community/static/v2/data.json"
        # https://data.sensor.community/static/v2/data.1h.json dati 1h
        # https://data.sensor.community/static/v2/data.json dati 5 min

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
        api_data = json.loads(api_request.content)
    except Exception as e:
        api_data = "Errore: C'è stato un qualche tipo di errore nel parsing del contenuto dell'URL. Forse è un problema del server."

    # voglio un solo record per ogni location
    target_area_output_data.objects.all().delete()


    # prende dati input e dispone in vettori le info di ognuna
    input_data = target_area_input_data.objects.all()

    


    # dai dati acquisiti, individua quelli che corrispondono al perimetro delle località selezionate, 
    # e salvane i valori
    for place in input_data:

        

        place_name = place.Name

        print("Inizio ricerca dati per %s..." % place_name)

        # predo lat e long e raggio della località input
        x_p = float(place.Longitude)
        y_p = float(place.Latitude)
        rho = 0.011300045235255235 * float(place.Radius) # fattore di trasformazione (coord/km)

        PM10_list = []
        PM25_list = []
        timestamp_list=[]
    
        for sensor in api_data:

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
                    timestamp_list.append(timestamp_value)  
                    print("    Timestamp: %s" % timestamp_value)                  

                else:
                    print("    Questo sensore non possiede dati di particolato")    

        # da qui in poi il  processi è lo stesso per diversi metodi di raccota dati

        n_selected_sensors = len (PM10_list)

        print("Valori del particolato raccolti da %s sensori per %s" % (n_selected_sensors, place_name))

        print("PM10:")
        print(PM10_list)  

        print("PM2.5:")
        print(PM25_list)  

        print("Ora delle rilevazioni:")
        print(timestamp_list) 

        n_selected_sensors = len(PM10_list)
        
        PM10_array = np.array(PM10_list)
        PM10_array = PM10_array.astype(np.float)

        PM25_array = np.array(PM25_list)
        PM25_array = PM25_array.astype(np.float)

        timestamp_array = np.array(timestamp_list)

        PM10_mean = round(np.mean(PM10_array), 2)
        PM25_mean = round(np.mean(PM25_array), 2)

        # col min prendo il tempo del sensore aggiornato meno di recente, per garanzia di aggiornamento minimo
        record_time = min(timestamp_array)
        # record_time = max(timestamp_array)
        
        # da solo non è necessario
        record_time = datetime.strptime(record_time, "%Y-%m-%d %H:%M:%S")

        # record_time = record_time.strftime("%d-%m-%Y %H:%M:%S")
        #  se lo metto dice che deve essere formattato in formato che mantega anche la timezone

        # passo in entrata un valore del pm e mi viene restituito in uscita il messaggio e la classe css corrispondente
        [PM10_quality, PM10_cathegory] = evaluate_PM10(PM10_mean)

        [PM25_quality, PM25_cathegory] = evaluate_PM10(PM25_mean)
 


            
        print("Valore medio del PM10 per %s: %s µg/m³. %s" % (place_name, PM10_mean, PM10_quality))
        print("Valore medio del PM2.5 per %s: %s µg/m³. %s" % (place_name, PM25_mean, PM25_quality))
        print("Timestamp delle osservazioni per %s: %s" % (place_name, record_time))


        new_record = target_area_output_data(
                                                Target_area_name=target_area_input_data.objects.get(Name=place_name),
                                                
                                                Latitude = place.Longitude,
                                                Longitude = place.Latitude,
                                                Radius = place.Radius,                                             
                                                
                                                Last_update_time=record_time,

                                                PM10_mean=PM10_mean,
                                                PM25_mean=PM25_mean,

                                                PM10_quality=PM10_quality, 
                                                PM25_quality=PM25_quality,

                                                PM10_cathegory=PM10_cathegory,
                                                PM25_cathegory=PM25_cathegory,

                                                n_selected_sensors=n_selected_sensors,
        )
        
        new_record.save()

        print("Dati per %s salvati nel modello!" % place_name)

        print("---------------------------------------------------")


    # quando ha processato tutti i posti
    print("---------------------------------------------------")

    # salvo tutto ciò che c'è nel modello output anche nel modello history
    save_in_history()


    # non ritorna niente perchè deve solo alvare in history

    # common_output = {
    #         'api_URL':api_URL, 
    #         'api_data':api_data, 
    #         'record_time':record_time,
    #         }

    # return common_output



