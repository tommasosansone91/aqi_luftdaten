from django.shortcuts import render

from pm_lookup.processing.realtime_processing_1 import get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoint

from .models import AreaParametersSet
from .models import RealtimeDatapoint
from .models import SerieParametersSet
from .models import ComputedSerie

from django.contrib.admin.views.decorators import staff_member_required




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
    
    #  ranna il processing senza rendere niente in una variabile
    get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoint()

    # va a prendere i dati nei modelli
    aree_di_interesse = AreaParametersSet.objects.all()    
    n_aree_di_interesse = AreaParametersSet.objects.all().count()    

    record_sensori = RealtimeDatapoint.objects.all()

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


