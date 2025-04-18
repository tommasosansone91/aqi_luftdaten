
# usage
#----------

# python manage.py test_save_current_pm_values_in_realtime_model

from django.core.management.base import BaseCommand

from pm_lookup.models import TargetArea, RealtimeDatapoints

import numpy as np 
import math

import time
from datetime import datetime

import json
import requests

from pm_lookup.processing.utils.air_quality_evaluators import evaluate_PM10, evaluate_PM25

"""this is just for development/test"""

# questo file lo richiamo solo se c'e l'ho in 
# app/management/commands/nome_file.py
# la linea from django.core.management.base import BaseCommand
# l'intestazione
# class Command(BaseCommand):
#     def handle(self, *args, **options):


class Command(BaseCommand):
    def handle(self, *args, **options):

        # RealtimeDatapoints.objects.all().delete()

        # url generating
        api_URL = "https://data.sensor.community/static/v2/data.1h.json"
            # https://data.sensor.community/static/v2/data.1h.json

        # go grab the api
        api_request = requests.get(api_URL)

        # save time
        record_time = datetime.now()

        # record parse
        try:
            # json parsa il contenuto di api_request in 
            api_data = json.loads(api_request.content)
        except json.JSONDecodeError as e:
            api_data = { "error_message": "Errore: il contenuto della risposta non è un JSON valido. ",
              "details": e
            }

        # prende dati input e dispone in vettori le info di ognuna
        input_data = TargetArea.objects.all()


        # dai dati acquisiti, individua quelli che corrispondono al perimetro delle località selezionate, 
        # e salvane i valori
        for place in input_data:

            place_name = place.name

            # predo lat e long e raggio della località input
            x_p = float(place.longitude)
            y_p = float(place.latitude)
            rho = float(place.radius)

            PM10_list = []
            PM25_list = []
        
            for sensor in api_data:

                x_s = float(sensor["location"]["longitude"])
                y_s = float(sensor["location"]["latitude"])
                            
                # termine 1 della formula
                t1 = math.sqrt( ( x_s - x_p )**2 + ( y_s - y_p )**2 )
                
                # termine 2 è rho

                if t1 <= rho:

                # allora estrai  le info del pm 

                    for physical_quantity_recorded in sensor['sensordatavalues']:

                        if physical_quantity_recorded['value_type'] == 'P1':

                            PM10_value = physical_quantity_recorded['value']               
                            PM10_list.append(PM10_value)

                        if physical_quantity_recorded['value_type'] == 'P2':

                            PM25_value = physical_quantity_recorded['value']                
                            PM25_list.append(PM25_value)

            # da qui in poi il  processi è lo stesso per diversi metodi di raccota dati

            print(PM10_list)  
            print(PM25_list)   

            number_of_contributing_sensors = len(PM10_list)
            
            PM10_array = np.array(PM10_list)
            PM10_array = PM10_array.astype(float)

            PM25_array = np.array(PM25_list)
            PM25_array = PM25_array.astype(float)

            PM10_mean = round(np.mean(PM10_array), 2)
            PM25_mean = round(np.mean(PM25_array), 2)

            # passo in entrata un valore del pm e mi viene restituito in uscita il messaggio e la classe css corrispondente
            [PM10_mean_cathegory_label, PM10_mean_cathegory] = evaluate_PM10(PM10_mean)

            [PM25_mean_cathegory_label, PM25_mean_cathegory] = evaluate_PM25(PM25_mean)



            new_record = RealtimeDatapoints(
                            target_area=TargetArea.objects.get(name=place_name),
                            last_update_time=record_time,

                            PM10_mean=PM10_mean,
                            PM25_mean=PM25_mean,

                            PM10_mean_cathegory_label=PM10_mean_cathegory_label,
                            PM25_mean_cathegory_label=PM25_mean_cathegory_label,
                            PM10_mean_cathegory=PM10_mean_cathegory,
                            PM25_mean_cathegory=PM25_mean_cathegory,

                            number_of_contributing_sensors=number_of_contributing_sensors,
                        )
            
            new_record.save()

        # quando ha processato tutti i posti

        context_dict = {
                'api_URL':api_URL, 
                'api_data':api_data, 
                'record_time':record_time,
                }

        return context_dict