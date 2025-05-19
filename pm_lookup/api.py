
# esportazione api
from django.http import JsonResponse
from datetime import datetime, timezone

from .models import AreaParametersSet
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import SerieParametersSet
from .models import ComputedSerie

from .processing.utils.air_quality_evaluators import evaluate_pollutant_concentration

from .processing.realtime_processing_1 import get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints

import ast

from django.utils.dateparse import parse_datetime



# list apis
#-----------

# ok
def areas_list_api(request):
    areas = AreaParametersSet.objects.all()
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
def sets_of_parameters_of_series_list_api(request):
    parameters_for_series = SerieParametersSet.objects.all()
    data = {
            "sets_of_parameters_of_series": list(
                parameters_for_series.values(
                    "pk",
                    "area_parameters_set",
                    "title",
                    "description",
                    "time_horizon",
                    "aggregation_period"
                    )
                )
            }
    response = JsonResponse(data)

    return response

# ok
# def realtime_datapoints_list_api(request):

#     # richiama il processign realtime che aggiorna i dati output
#     get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints()

#     rt_records = RealtimeDatapoints.objects.all()
#     data = {"realtime_records": list(rt_records.values())}
#     # lasciare vuota la coppia di parentesi dopo values vuol dire includere tutti i valori, 
#     # ma la parentesi deve esistere
#     response = JsonResponse(data)

#     return response


# multifilter apis
#-------------------

def historical_datapoints_subset_api(request):

    area_parameters_set = request.GET.get('area_parameters_set')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not (area_parameters_set and start_date and end_date):
        return JsonResponse(
            {"error": "area_parameters_set, start_date e end_date sono obbligatori."},
            status=400
        )

    try:
        start_date = parse_datetime(start_date)
        end_date = parse_datetime(end_date)

    except Exception:
        return JsonResponse(
            {
                "error": "Formato data non valido. Usa ISO 8601 (es. {}).".format( datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') )
            },
            status=400
        )

    datapoints_subset = HistoricalDatapoints.objects.filter(
        area_parameters_set=area_parameters_set,
        last_update_time__gte=start_date,
        last_update_time__lte=end_date
    )

    list_of_datapoints = []

    for dp in datapoints_subset:
        list_of_datapoints.append(
            {
            
            "area_parameters_set": dp.area_parameters_set.id,
            "last_update_time": dp.last_update_time.isoformat(),
            
            "PM10_mean": dp.PM10_mean,
            "PM25_mean": dp.PM25_mean,

            "PM10_mean_cathegory_label" : evaluate_pollutant_concentration("PM10", dp.PM10_mean)[0],
            "PM25_mean_cathegory_label"  : evaluate_pollutant_concentration("PM25", dp.PM10_mean)[0],

            "PM10_mean_cathegory_value" : evaluate_pollutant_concentration("PM10", dp.PM10_mean)[1],
            "PM25_mean_cathegory_value" : evaluate_pollutant_concentration("PM25", dp.PM10_mean)[1],

            "number_of_contributing_sensors": dp.number_of_contributing_sensors,
            "uuid": str(dp.uuid),

            }
        )

    data = {
            "historical_datapoints_subset": list_of_datapoints
            }

    response = JsonResponse(data, safe=False)

    return response


# detail apis
#--------------


def area_detail_api(request, pk):

    try:
        area = AreaParametersSet.objects.get(pk=pk)
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
        response = JsonResponse(data)

    except AreaParametersSet.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "area_parameters_set non trovata. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response


def parameters_for_serie_detail_api(request, pk):

    try:
        parameters_set = SerieParametersSet.objects.get(pk=pk)
        data = {
                # "parameters_set":dict(parameters_set).items()
                "set_of_parameters_of_serie":
                    {
                        "pk":parameters_set.area_parameters_set.pk,
                        "area_parameters_set":parameters_set.area_parameters_set.pk,
                        "title":parameters_set.title,
                        "description":parameters_set.description,
                        "time_horizon":parameters_set.time_horizon,
                        "aggregation_period":parameters_set.aggregation_period,
                    }        
                } 
        response = JsonResponse(data)

    except SerieParametersSet.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "serie_parameters_set non trovato. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response


# api/realtime_datapoints_detail/<int:pk>
def realtime_datapoint_detail_api(request, pk):

    get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints()

    # substitute with using the most recent in historical
    # and do the vaulation with the helper

    try:
        area = AreaParametersSet.objects.get(pk=pk)
        # confidando che ne prenda solo uno, il get è sulla pk!

        realtime_datapoint = RealtimeDatapoints.objects.get(area_parameters_set=area)

        data = {
                # "area":dict(area).items()
                "realtime_datapoint":
                    {   
                        # così la pk per richiamare
                        "pk":realtime_datapoint.area_parameters_set.pk,

                        # # dati della area associata
                        # "name":realtime_datapoint.area_parameters_set.name,
                        # "longitude":realtime_datapoint.area_parameters_set.longitude,
                        # "latitude":realtime_datapoint.area_parameters_set.latitude,
                        # "radius":realtime_datapoint.area_parameters_set.radius,

                        # dati della rilevazione                        
                        "last_update_time" : realtime_datapoint.last_update_time, 

                        "PM10_mean" : realtime_datapoint.PM10_mean,
                        "PM25_mean" : realtime_datapoint.PM25_mean, 

                        "PM10_mean_cathegory_label" : evaluate_pollutant_concentration("PM10", realtime_datapoint.PM10_mean)[0],
                        "PM25_mean_cathegory_label"  : evaluate_pollutant_concentration("PM25", realtime_datapoint.PM10_mean)[0],

                        "PM10_mean_cathegory_value" : evaluate_pollutant_concentration("PM10", realtime_datapoint.PM10_mean)[1],
                        "PM25_mean_cathegory_value" : evaluate_pollutant_concentration("PM25", realtime_datapoint.PM10_mean)[1],

                        "number_of_contributing_sensors" : realtime_datapoint.number_of_contributing_sensors,


                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)

    except AreaParametersSet.DoesNotExist:
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "area_parameters_set oppure realtime_datapoint non trovati. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response



# api/computed_series_detail/<int:pk>
def computed_serie_detail_api(request, pk):

    try:
        # the pk is the parameters set one
        parameters_set = SerieParametersSet.objects.get(pk=pk)
        computed_serie = ComputedSerie.objects.get(serie_parameters_set=parameters_set)
        
        # this has to be turned to json
        PM10_mean_values = ast.literal_eval(computed_serie.PM10_mean_values)
        PM25_mean_values = ast.literal_eval(computed_serie.PM25_mean_values)

        PM10_mean_cathegory_label_values = [ evaluate_pollutant_concentration("PM10", i)[0] for i in PM10_mean_values ]
        PM25_mean_cathegory_label_values = [ evaluate_pollutant_concentration("PM25", i)[0] for i in PM25_mean_values ]
        PM10_mean_cathegory_values = [ evaluate_pollutant_concentration("PM10", i)[1] for i in PM10_mean_values ]
        PM25_mean_cathegory_values = [ evaluate_pollutant_concentration("PM25", i)[1] for i in PM25_mean_values ]
        
        data = {
                # "area":dict(area).items()
                "computed_serie":
                    {   
                        # così la pk per richiamare
                        "pk" : computed_serie.serie_parameters_set.area_parameters_set.pk,

                        # dati della area associata
                        "name" : computed_serie.serie_parameters_set.area_parameters_set.name,
                        "longitude" : computed_serie.serie_parameters_set.area_parameters_set.longitude,
                        "latitude" : computed_serie.serie_parameters_set.area_parameters_set.latitude,
                        "radius" : computed_serie.serie_parameters_set.area_parameters_set.radius,

                        # dati del serie_parameters_set associati

                        # dati della rilevazione                        
                        "computed_serie_time_values" : computed_serie.record_time_values, 

                        "PM10_mean_values" : computed_serie.PM10_mean_values,
                        "PM25_mean_values" : computed_serie.PM25_mean_values, 

                        "PM10_mean_cathegory_label_values" : PM10_mean_cathegory_label_values,
                        "PM25_mean_cathegory_label_values"  : PM25_mean_cathegory_label_values,

                        "PM10_mean_cathegory_values" : PM10_mean_cathegory_values,
                        "PM25_mean_cathegory_values" : PM25_mean_cathegory_values,

                        "n_selected_sensor_values" : computed_serie.number_of_contributing_sensors_values,

                        "PM10_graph_div" : computed_serie.PM10_graph_div,
                        "PM25_graph_div" : computed_serie.PM25_graph_div,

                    }        
                } 
        # stavolta non ho bisogno di listare perchè i valori che cerco sono in un singolo dizionario, non in una lista di dizionari
        response = JsonResponse(data)

    except (SerieParametersSet.DoesNotExist, ComputedSerie.DoesNotExist):
        # allora devo inserire nella risposta json un messaggio di errore
        response = JsonResponse(
            {
            "error":{
                    "code":404,
                    "message": "serie_parameters_set oppure computed_serie non trovati. Verifica la correttezza dei parametri in input."
                    }
            },
            status=404 # questo messaggio d'errore serve al frontend framework
        )
    
    return response

