
# esportazione api
from django.http import JsonResponse

from .models import TargetArea
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import DatapointsSerieParameters
from .models import DatapointsSerieComputed

from .processing.realtime_processing_1 import get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints


# list apis
#-----------

# ok
def areas_list_api(request):
    areas = TargetArea.objects.all()
    data = {
            "areas": list(
                areas.values(
                    "pk",
                    "name",
                    "longitude",
                    "latitude",
                    "radius"
                    )
                )
            }
    response = JsonResponse(data)
    return response

# ok
def parameters_for_series_list_api(request):
    parameters_for_series = DatapointsSerieParameters.objects.all()
    data = {
            "parameters_for_series": list(
                parameters_for_series.values(
                    "pk",
                    "target_area",
                    "title",
                    "description",
                    "time_horizon"
                    "aggregation_period"
                    )
                )
            }
    response = JsonResponse(data)
    return response

# ok
def realtime_datapoints_list_api(request):

    # richiama il processign realtime che aggiorna i dati output
    get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints()

    rt_records = RealtimeDatapoints.objects.all()
    data = {"realtime_records": list(rt_records.values())}
    # lasciare vuota la coppia di parentesi dopo values vuol dire includere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response

# mutlifilter apis
#-------------------

def historical_data_subset_api(request):
    h_records = HistoricalDatapoints.objects.all()
    # fitler
    data = {
            "historical_records_subset": list(
                    h_records.values()
                )
            }
    # lasciare vuota la coppia di parentesi dopo values vuol dire accludere tutti i valori, 
    # ma la parentesi deve esistere
    response = JsonResponse(data)
    return response


# detail apis
#--------------


def area_detail_api(request, pk):

    try:
        area = TargetArea.objects.get(pk=pk)
        
        data = {
                # "area":dict(area).items()

                "area":
                    {
                        "pk":area.pk,
                        "name":area.name,
                        "longitude":area.longitude,
                        "latitude":area.latitude,
                        "radius":area.radius,

                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except area.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "area non trovata. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response


def parameters_for_serie_detail_api(request, pk):

    try:
        parameters_set = DatapointsSerieParameters.objects.get(pk=pk)
        
        data = {
                # "parameters_set":dict(parameters_set).items()

                "parameters_set":
                    {
                        "pk":parameters_set.target_area,
                        "name":parameters_set.title,
                        "longitude":parameters_set.description,
                        "latitude":parameters_set.time_horizon,
                        "radius":parameters_set.aggregation_period,

                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except parameters_set.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "set di parametri non trovato. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response


# api/realtime_datapoints_detail/<int:pk>
def realtime_datapoints_detail_api(request, pk):

    get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints()

    try:
        area = TargetArea.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        record = RealtimeDatapoints.objects.get(TargetArea=area)

      
        data = {
                # "area":dict(area).items()

                "record":
                    {   
                        # così la pk per richiamare
                        "pk":record.target_area.pk,

                        # dati della area associata
                        "name":record.target_area.name,
                        "longitude":record.target_area.longitude,
                        "latitude":record.target_area.latitude,
                        "radius":record.target_area.radius,

                        # dati della rilevazione                        
                        "last_update_time" : record.last_update_time, 

                        "PM10_mean" : record.PM10_mean,
                        "PM25_mean" : record.PM25_mean, 

                        "PM10_mean_cathegory_label" : record.PM10_mean_cathegory_label,
                        "PM25_mean_cathegory_label"  : record.PM25_mean_cathegory_label,

                        "PM10_mean_cathegory_values" : record.PM10_mean_cathegory,
                        "PM25_mean_cathegory_values" : record.PM25_mean_cathegory,

                        "number_of_contributing_sensors" : record.number_of_contributing_sensors,


                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except area.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "area oppure record non trovati. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response





# api/computed_series_detail/<int:pk>
def computed_serie_detail_api(request, pk):

    try:
        parameters_set = DatapointsSerieParameters.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        computed_serie = DatapointsSerieComputed.objects.get(datapoints_serie_parameters=parameters_set)

      
        data = {
                # "area":dict(area).items()

                "computed_serie":
                    {   
                        # così la pk per richiamare
                        "pk":computed_serie.datapoints_serie_parameters.target_area.pk,

                        # dati della area associata
                        "name":computed_serie.datapoints_serie_parameters.target_area.name,
                        "longitude":computed_serie.datapoints_serie_parameters.target_area.longitude,
                        "latitude":computed_serie.datapoints_serie_parameters.target_area.latitude,
                        "radius":computed_serie.datapoints_serie_parameters.target_area.radius,

                        # dati del set di parametri associati

                        # dati della rilevazione                        
                        "computed_serie_time_values" : computed_serie.record_time_values, 

                        "PM10_mean_values" : computed_serie.PM10_mean_values,
                        "PM25_mean_values" : computed_serie.PM25_mean_values, 

                        # "PM10_mean_cathegory_label_values" : computed_serie.PM10_mean_cathegory_label_values,
                        # "PM25_mean_cathegory_label_values"  : computed_serie.PM25_mean_cathegory_label_values,

                        # "PM10_mean_cathegory_values" : computed_serie.PM10_mean_cathegory_values,
                        # "PM25_mean_cathegory_values" : computed_serie.PM25_mean_cathegory_values,

                        "n_selected_sensor_values" : computed_serie.number_of_contributing_sensors_values,

                        "PM10_graph_div" : computed_serie.PM10_graph_div,
                        "PM25_graph_div" : computed_serie.PM25_graph_div,

                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)
        return response

    except (parameters_set.DoesNotExist, computed_serie.DoesNotExist):
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "area oppure computed_serie non trovati. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response

