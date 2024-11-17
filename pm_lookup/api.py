
# esportazione api
from django.http import JsonResponse

from .models import TargetArea
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import DatapointsSerieParameters
from .models import DatapointsSerieComputed

from .processing.realtime_processing_1 import get_current_pm_values_and_save_them_in_RealtimeDatapoints



def cities_list_api(request):
    cities = TargetArea.objects.all()
    data = {"cities":list(cities.values("pk","name","longitude","latitude","radius"))}
    response = JsonResponse(data)
    return response

def cities_RealtimeDatapoints_api(request):

    # richiama il processign realtime che aggiorna i dati output
    get_current_pm_values_and_save_them_in_RealtimeDatapoints()

    rt_records = RealtimeDatapoints.objects.all()
    data = {"realtime_records":list(rt_records.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


def historical_data_api(request):
    h_records = HistoricalDatapoints.objects.all()
    data = {"historical_records":list(h_records.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


def time_series_api(request):
    h_series = DatapointsSerieParameters.objects.all()
    data = {"time_series":list(h_series.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


def daily_time_series_api(request):
    d_series = DatapointsSerieComputed.objects.all()
    data = {"daily_time_series":list(d_series.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response

# le viste api qui sotto hanno le i dati filterati per città, e poi limitati a 24*30, per ogni città

def city_detail_api(request, pk):

    try:
        city = TargetArea.objects.get(pk=pk)
        
        data = {
                # "city":dict(city).items()

                "city":
                    {
                        "pk":city.pk,
                        "name":city.name,
                        "longitude":city.longitude,
                        "latitude":city.latitude,
                        "radius":city.radius,

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


# api/RealtimeDatapoints_detail/<int:pk>
def RealtimeDatapoints_detail_api(request, pk):

    get_current_pm_values_and_save_them_in_RealtimeDatapoints()

    try:
        city = TargetArea.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        record = RealtimeDatapoints.objects.get(TargetArea=city)

      
        data = {
                # "city":dict(city).items()

                "record":
                    {   
                        # così la pk per richiamare
                        "pk":record.TargetArea.pk,

                        # dati della città associata
                        "name":record.TargetArea.name,
                        "longitude":record.TargetArea.longitude,
                        "latitude":record.TargetArea.latitude,
                        "radius":record.TargetArea.radius,

                        # dati della rilevazione                        
                        "last_update_time" : record.last_update_time, 

                        "PM10_mean" : record.PM10_mean,
                        "PM25_mean" : record.PM25_mean, 

                        "PM10_mean_quality_cathegory_label" : record.PM10_mean_quality_cathegory_label,
                        "PM25_mean_quality_cathegory_label"  : record.PM25_mean_quality_cathegory_label,

                        "PM10_mean_quality_cathegory" : record.PM10_mean_quality_cathegory,
                        "PM25_mean_cathegory" : record.PM25_mean_cathegory,

                        "number_of_contributing_sensors" : record.number_of_contributing_sensors,


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
#         city = TargetArea.objects.get(pk=pk)
#         # ne prende molti

#         record = RealtimeDatapoints.objects.get(TargetArea=city)

      
#         data = {
#                 # "city":dict(city).items()

#                 "record":
#                     {   
#                         # così la pk per richiamare
#                         "pk":record.TargetArea.pk,

#                         # dati della città associata
#                         "name":record.TargetArea.name,
#                         "longitude":record.TargetArea.longitude,
#                         "latitude":record.TargetArea.latitude,
#                         "radius":record.TargetArea.radius,

#                         # dati della rilevazione                        
#                         "last_update_time" : record.last_update_time, 

#                         "PM10_mean" : record.PM10_mean,
#                         "PM25_mean" : record.PM25_mean, 

#                         "PM10_mean_quality_cathegory_label" : record.PM10_mean_quality_cathegory_label,
#                         "PM25_mean_quality_cathegory_label"  : record.PM25_mean_quality_cathegory_label,

#                         "PM10_mean_quality_cathegory" : record.PM10_mean_quality_cathegory,
#                         "PM25_mean_cathegory" : record.PM25_mean_cathegory,

#                         "number_of_contributing_sensors" : record.number_of_contributing_sensors,


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



    
# api/time_series_detail/<int:pk>
def time_serie_detail_api(request, pk):

    try:
        city = TargetArea.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        record = DatapointsSerieParameters.objects.get(TargetArea=city)

      
        data = {
                # "city":dict(city).items()

                "time_serie":
                    {   
                        # così la pk per richiamare
                        "pk":record.TargetArea.pk,

                        # dati della città associata
                        "name":record.TargetArea.name,
                        "longitude":record.TargetArea.longitude,
                        "latitude":record.TargetArea.latitude,
                        "radius":record.TargetArea.radius,

                        # dati della rilevazione                        
                        "record_time_values" : record.record_time_values, 

                        "PM10_mean_values" : record.PM10_mean_values,
                        "PM25_mean_values" : record.PM25_mean_values, 

                        "PM10_mean_quality_cathegory_label_values" : record.PM10_mean_quality_cathegory_label_values,
                        "PM25_mean_quality_cathegory_label_values"  : record.PM25_mean_quality_cathegory_label_values,

                        "PM10_mean_quality_cathegory_values" : record.PM10_mean_quality_cathegory_values,
                        "PM25_mean_cathegory_values" : record.PM25_mean_cathegory_values,

                        "n_selected_sensor_values" : record.number_of_contributing_sensors_values,

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





# api/daily_time_series_detail/<int:pk>
def daily_time_serie_detail_api(request, pk):

    try:
        city = TargetArea.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        record = DatapointsSerieComputed.objects.get(TargetArea=city)

      
        data = {
                # "city":dict(city).items()

                "daily_time_serie":
                    {   
                        # così la pk per richiamare
                        "pk":record.TargetArea.pk,

                        # dati della città associata
                        "name":record.TargetArea.name,
                        "longitude":record.TargetArea.longitude,
                        "latitude":record.TargetArea.latitude,
                        "radius":record.TargetArea.radius,

                        # dati della rilevazione                        
                        "record_time_values" : record.record_time_values, 

                        "PM10_mean_values" : record.PM10_mean_values,
                        "PM25_mean_values" : record.PM25_mean_values, 

                        "PM10_mean_quality_cathegory_label_values" : record.PM10_mean_quality_cathegory_label_values,
                        "PM25_mean_quality_cathegory_label_values"  : record.PM25_mean_quality_cathegory_label_values,

                        "PM10_mean_quality_cathegory_values" : record.PM10_mean_quality_cathegory_values,
                        "PM25_mean_cathegory_values" : record.PM25_mean_cathegory_values,

                        "n_selected_sensor_values" : record.number_of_contributing_sensors_values,

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