
import numpy as np 

def get_pm():    
    
    import json
    
    # va su internet, prende le API e le porta indietro
    import requests

    # go grab the api

    # api method
    Luftdaten_API_method = "area"

    # rea method parameters
    center_lat = 45.464211

    #wgs84
    center_long = 9.191383 #wgs84
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
      



    context_dict = {
                    'radius':radius, 
                    'center_lat':center_lat,
                    'center_long':center_long,

                    'api_URL':api_URL, 
                    'api':api, 

                    'PM10_mean':PM10_mean, 
                    'PM25_mean':PM25_mean, 

                    'PM10_quality':PM10_quality, 
                    'PM25_quality':PM25_quality,

                    'PM10_cathegory':PM10_cathegory,
                    'PM25_cathegory':PM25_cathegory
                    }

    return context_dict