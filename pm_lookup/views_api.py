
# esportazione api
from django.http import JsonResponse

from .models import target_area_input_data
from .models import target_area_output_data
from .models import target_area_history_data


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