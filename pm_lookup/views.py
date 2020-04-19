from django.shortcuts import render
import numpy as np

# Create your views here.

# ogni volta che un user va su un sito e clicca su un url sta facendo una request

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def valori_particolato(request):
    import json
    
    # va su internet, prende le API e le porta indietro
    import requests

    # go grab the api

    # api method
    Luftdaten_API_method = "area"

    # rea method parameters
    center_lat = 45.463704 #wgs84
    center_long = 9.187689 #wgs84
    radius = 8 #km

    # switch
    if Luftdaten_API_method == "area":

        api_URL = "https://data.sensor.community/airrohr/v1/filter/area=" + str(center_lat) + "," + str(center_long) + "," +  str(radius)

        api_request = requests.get(api_URL)

        

        # https://data.sensor.community/airrohr/v1/filter/area=45.463704,9.187689,10
    

    # È possibile utilizzare delle funzioni di concatena 
    #  per cambiare programmaticamente Come scritto l'URL 
    # e quindi cambiare il valore che viene ritornato dalle api 

    try:
        # json parsa il contenuto di api_request in 
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Errore: C'è stato un qualche tipo di errore nel parsing del contenuto dell'URL. Forse è un problema del server."

    # print("L'URL selezionato per le AP e parsato in Json ritorna:")
    # print(api)


    # per ogni dizionario nella lista

        # tira fuori P1
        # tira fuori P2

    PM10_list = []
    PM25_list = []


    api_data = api

    for sensor in api_data:

        for physical_quantity_recorded in sensor['sensordatavalues']:

            if physical_quantity_recorded['value_type'] == 'P1':

                PM10_value = physical_quantity_recorded['value']               
                PM10_list.append(PM10_value)

            if physical_quantity_recorded['value_type'] == 'P2':

                PM25_value = physical_quantity_recorded['value']                
                PM25_list.append(PM25_value)





    print(PM10_list)  
    print(PM25_list)   

    
    PM10_array = np.array(PM10_list)
    PM10_array = PM10_array.astype(np.float)

    PM25_array = np.array(PM25_list)
    PM25_array = PM25_array.astype(np.float)


    PM10_mean = round(np.mean(PM10_array), 2)
    PM25_mean = round(np.mean(PM25_array), 2)

    context_dict = {'api_URL':api_URL, 'api':api, 'PM10_mean':PM10_mean, 'PM25_mean':PM25_mean}

    return render(request, 'valori_particolato.html', context_dict)