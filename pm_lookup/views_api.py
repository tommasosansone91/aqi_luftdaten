
# esportazione api
from django.http import JsonResponse

from .models import target_area_input_data
from .models import target_area_output_data
from .models import target_area_history_data
from .models import target_area_history_serie


def cities_list_api(request):
    cities = target_area_input_data.objects.all()
    data = {"cities":list(cities.values("pk","Name","Longitude","Latitude","Radius"))}
    response = JsonResponse(data)
    return response

def realtime_data_api(request):

    # richiama il processign realtime che aggiorna i dati output

    rt_records = target_area_output_data.objects.all()
    data = {"realtime_records":list(rt_records.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


def historical_data_api(request):
    h_records = target_area_history_data.objects.all()
    data = {"historical_records":list(h_records.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


def historical_series_api(request):
    h_series = target_area_history_serie.objects.all()
    data = {"historical_series":list(h_series.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


# le viste api qui sotto hanno le i dati filterati per città, e poi limitati a 24*30, per ogni città

def city_detail_api(request, pk):

    try:
        city = target_area_input_data.objects.get(pk=pk)
        
        data = {
                # "city":dict(city).items()

                "city":
                    {
                        "pk":city.pk,
                        "Name":city.Name,
                        "Longitude":city.Longitude,
                        "Latitude":city.Latitude,
                        "Radius":city.Radius,

                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except city.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "Città non trovata. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response


# api/realtime_data_detail/<int:pk>
def realtime_data_detail_api(request, pk):

    try:
        city = target_area_input_data.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        record = target_area_output_data.objects.get(Target_area_input_data=city)

      
        data = {
                # "city":dict(city).items()

                "record":
                    {   
                        # così la pk per richiamare
                        "pk":record.Target_area_input_data.pk,

                        # dati della città associata
                        "Name":record.Target_area_input_data.Name,
                        "Longitude":record.Target_area_input_data.Longitude,
                        "Latitude":record.Target_area_input_data.Latitude,
                        "Radius":record.Target_area_input_data.Radius,

                        # dati della rilevazione                        
                        "Last_update_time" : record.Last_update_time, 

                        "PM10_mean" : record.PM10_mean,
                        "PM25_mean" : record.PM25_mean, 

                        "PM10_quality" : record.PM10_quality,
                        "PM25_quality"  : record.PM25_quality,

                        "PM10_cathegory" : record.PM10_cathegory,
                        "PM25_cathegory" : record.PM25_cathegory,

                        "n_selected_sensors" : record.n_selected_sensors,


                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except city.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "Città oppure record non trovati. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response



# deve attingere da un modello serie storica

# api/historical_data_detail/<int:pk>
# def historical_data_detail_api(request, pk):

#     try:
#         city = target_area_input_data.objects.get(pk=pk)
#         # ne prende molti

#         record = target_area_output_data.objects.get(Target_area_input_data=city)

      
#         data = {
#                 # "city":dict(city).items()

#                 "record":
#                     {   
#                         # così la pk per richiamare
#                         "pk":record.Target_area_input_data.pk,

#                         # dati della città associata
#                         "Name":record.Target_area_input_data.Name,
#                         "Longitude":record.Target_area_input_data.Longitude,
#                         "Latitude":record.Target_area_input_data.Latitude,
#                         "Radius":record.Target_area_input_data.Radius,

#                         # dati della rilevazione                        
#                         "Last_update_time" : record.Last_update_time, 

#                         "PM10_mean" : record.PM10_mean,
#                         "PM25_mean" : record.PM25_mean, 

#                         "PM10_quality" : record.PM10_quality,
#                         "PM25_quality"  : record.PM25_quality,

#                         "PM10_cathegory" : record.PM10_cathegory,
#                         "PM25_cathegory" : record.PM25_cathegory,

#                         "n_selected_sensors" : record.n_selected_sensors,


#                     }        
#                 } 
#         # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
#         response = JsonResponse(data)
#         return response

#     except city.DoesNotExist:
#         # allora devo inserire nella risposta json un messaggio di errore
#         response = JsonResponse(
#             {
#             "error":{
#                     "code":404,
#                     "message": "Città oppure record non trovati. Verifica la correttezza dei parametri in input."
#                     }
#             },
#             status=404 # questo messaggio d'errore serve al frontend framework
#         )
    
#     return response



    
    # api/historical_series_detail/<int:pk>
def historical_series_detail_api(request, pk):

    try:
        city = target_area_input_data.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        record = target_area_history_serie.objects.get(Target_area_input_data=city)

      
        data = {
                # "city":dict(city).items()

                "time_serie":
                    {   
                        # così la pk per richiamare
                        "pk":record.Target_area_input_data.pk,

                        # dati della città associata
                        "Name":record.Target_area_input_data.Name,
                        "Longitude":record.Target_area_input_data.Longitude,
                        "Latitude":record.Target_area_input_data.Latitude,
                        "Radius":record.Target_area_input_data.Radius,

                        # dati della rilevazione                        
                        "Record_time_values" : record.Record_time_values, 

                        "PM10_mean_values" : record.PM10_mean_values,
                        "PM25_mean_values" : record.PM25_mean_values, 

                        "PM10_quality_values" : record.PM10_quality_values,
                        "PM25_quality_values"  : record.PM25_quality_values,

                        "PM10_cathegory_values" : record.PM10_cathegory_values,
                        "PM25_cathegory_values" : record.PM25_cathegory_values,

                        "n_selected_sensor_values" : record.n_selected_sensors_values,

                        "PM10_graph_div" : record.PM10_graph_div,
                        "PM25_graph_div" : record.PM25_graph_div,

                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except city.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "Città oppure record non trovati. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response