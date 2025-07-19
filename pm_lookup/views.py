from django.shortcuts import render

from pm_lookup.processing.utils.sensors_network_data_processing import extract_data_from_sensors_network_for_all_places

from .models import AreaParametersSet
from .models import SerieParametersSet
from .models import ComputedSerie

from django.contrib.admin.views.decorators import staff_member_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now


# Create your views here.

# ogni volta che un user va su un sito e clicca su un url sta facendo una request

def home(request):
    return render(request, 'home.html', {})

def catalogo_api(request):
    return render(request, 'catalogo_api.html', {})

# def about(request):
#     return render(request, 'about.html', {})

# def particolato_milano(request):
    
#     context_dict = get_single_location_pm()

#     return render(request, 'particolato_milano.html', context_dict)

#------------------

# these two functions are invoked in the api page, but they are views, 
# since they display userfriendly data to the user


def catalogo_aree_interesse(request):

    aree_di_interesse = AreaParametersSet.objects.all().order_by('id')
    # from AreaParametersSet select *, order by id

    context_dict =  {'aree_di_interesse':aree_di_interesse}

    return render(request, 'catalogo_aree_interesse.html', context_dict)


def catalogo_set_parametri_definizione_serie_storiche(request):

    sets_parametri_serie_storiche = SerieParametersSet.objects.all().order_by('id')
    # from SerieParametersSet select *, order by id

    context_dict =  {'sets_parametri_serie_storiche':sets_parametri_serie_storiche}

    return render(request, 'catalogo_set_parametri_definizione_serie_storiche.html', context_dict)

#-------------------

def valori_realtime(request):

    # va a prendere i dati nei modelli
    aree_di_interesse = AreaParametersSet.objects.all()    
    n_aree_di_interesse = AreaParametersSet.objects.all().count()  

    record_sensori = extract_data_from_sensors_network_for_all_places()["processed_data_for_all_places"]

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }

    return render(request, 'valori_realtime.html', context_dict)


# solo raffigurazione
def grafici_serie_storiche(request):

    print("Richiamo dati in ComputedSerie...")

    datapoints_serie_computed = ComputedSerie.objects.filter(
        serie_parameters_set__show_serie=True
    )

    print("Dati in ComputedSerie acquisiti!")

    n_aree_di_interesse = AreaParametersSet.objects.all().count()    
    n_serie = SerieParametersSet.objects.all().count()

    context_dict = {
        "datapoints_serie_computed": datapoints_serie_computed,
        'n_aree_di_interesse':n_aree_di_interesse,
        'n_serie': n_serie
    }

    print("Dati in trasmissione al template!")

    return render(request, 'grafici_serie_storiche.html', context_dict)


# custom messages system view
#----------------------------------

_messages = []

@csrf_exempt
def publish_message(request):
    print("publishing messages...")
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

            text = data.get("text")
            color = data.get("background_color", "#ffffff")  # default: white
            timestamp = data.get(
                "timestamp", 
                now().isoformat()  # Django-aware timestamp
            ) 

            if text:
                _messages.append(
                    {
                    "timestamp": timestamp,  
                    "text": text,
                    "background_color": color
                    }
                )
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"error": "No message provided"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"status": "error"}, status=400)


def get_messages(request):
    print("getting messages...")
    return JsonResponse({"messages": _messages})


def message_display_page(request):
    return render(request, 'messaging_system/message.html')

