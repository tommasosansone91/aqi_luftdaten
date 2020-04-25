
import numpy as np 
import math

import time
from datetime import datetime

import json
import requests

from .models import target_area_input_data, target_area_output_data



def get_pm_2():    

    
    # url generating
    api_URL = "https://data.sensor.community/static/v2/data.1h.json"
        # https://data.sensor.community/static/v2/data.1h.json

    print("In attesa di ricevere i dati...")

    # go grab the api
    api_request = requests.get(api_URL)

    # save time
    record_time = datetime.now()

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

        # predo lat e long e raggio della località input
        x_p = float(place.Longitude)
        y_p = float(place.Latitude)
        rho = 0.011300045235255235 * float(place.Radius) # fattore di trasformazione (coord/km)

        PM10_list = []
        PM25_list = []
    
        for sensor in api_data:

            x_s = float(sensor["location"]["longitude"])
            y_s = float(sensor["location"]["latitude"])

            # print("Latitudine e longitudine del sensore in esame: %s, %s" % (y_s, x_s) )
                        
            # termine 1 della formula

            t1 = math.sqrt( ( x_s - x_p )**2 + ( y_s - y_p )**2 )

            # termine 2 è rho

            if t1 <= rho:

            # no perchè latitudine longitudine e rho non hanno la stessa unità di misura
            # ho convertito il raggio in lat e logn-- 8km ~~ 0.043702 .... per milano



                print("Trovato un sensore entro l'area definita per %s" % place_name)
                print("Latitudine e longitudine del sensore in esame: %s, %s" % (y_s, x_s) )

                # allora estrai  le info del pm 

                for physical_quantity_recorded in sensor['sensordatavalues']:

                    if physical_quantity_recorded['value_type'] == 'P1':

                        PM10_value = physical_quantity_recorded['value']               
                        PM10_list.append(PM10_value)

                    if physical_quantity_recorded['value_type'] == 'P2':

                        PM25_value = physical_quantity_recorded['value']                
                        PM25_list.append(PM25_value)

        # da qui in poi il  processi è lo stesso per diversi metodi di raccota dati

        n_selected_sensors = len(PM10_list)

        print("Valori del particolato raccolti da %s sensori per %s" % (n_selected_sensors, place_name))

        print(PM10_list)  
        print(PM25_list)   

        n_selected_sensors = len(PM10_list)
        
        PM10_array = np.array(PM10_list)
        PM10_array = PM10_array.astype(np.float)

        PM25_array = np.array(PM25_list)
        PM25_array = PM25_array.astype(np.float)

        PM10_mean = round(np.mean(PM10_array), 2)
        PM25_mean = round(np.mean(PM25_array), 2)




        # categorie di qualità dell'aria rispetto a PM 10
        if PM10_mean <=20:
            PM10_quality="Ottima"
            PM10_cathegory="prima"

        elif PM10_mean>=20 and PM10_mean <=35:
            PM10_quality="Buona"
            PM10_cathegory="seconda"
        
        elif PM10_mean>=35 and PM10_mean <=50:
            PM10_quality="Al limite dell'accettabilità"
            PM10_cathegory="terza"

        elif PM10_mean>=50 and PM10_mean <=100:
            PM10_quality="Fuori legge"
            PM10_cathegory="quarta"

        elif PM10_mean>=100 and PM10_mean <=200:
            PM10_quality="Pericolosa"
            PM10_cathegory="quita"

        elif PM10_mean>=200:
            PM10_quality="Emergenza evacuazione"
            PM10_cathegory="sesta"

        else:
            PM10_quality="No data"
            PM10_cathegory="nessuna"


        # categorie di qualità dell'aria rispetto a PM 2.5
        if PM25_mean <=10:
            PM25_quality="Ottima"
            PM25_cathegory="prima"

        elif PM25_mean>=10 and PM25_mean <=20:
            PM25_quality="Buona"
            PM25_cathegory="seconda"
        
        elif PM25_mean>=20 and PM25_mean <=25:
            PM25_quality="Al limite dell'accettabilità"
            PM25_cathegory="terza"

        elif PM25_mean>=25 and PM25_mean <=50:
            PM25_quality="Fuori legge"
            PM25_cathegory="quarta"

        elif PM25_mean>=50 and PM25_mean <=100:
            PM25_quality="Pericolosa"
            PM25_cathegory="quinta"

        elif PM25_mean>=100:
            PM25_quality="Emergenza evacuazione"
            PM25_cathegory="sesta"

        else:
            PM25_quality="No data"
            PM25_cathegory="nessuna"

            
        print("Valore medio del PM10 per %s: %s µg/m³. %s" % (place_name, PM10_mean, PM10_quality))
        print("Valore medio del PM2.5 per %s: %s µg/m³. %s" % (place_name, PM25_mean, PM25_quality))


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

        print("Salvati i dati per %s" % place_name)

    # quando ha processato tutti i posti

    common_output = {
            'api_URL':api_URL, 
            'api_data':api_data, 
            'record_time':record_time,
            }

    return common_output