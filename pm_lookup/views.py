from django.shortcuts import render

from pm_lookup.processing.realtime_processing import get_realtime_pm
from pm_lookup.processing.realtime_plus_history_processing import get_realtime_and_save_history_pm

from .models import target_area_input_data
from .models import target_area_realtime_data
from .models import target_area_history_data
from .models import target_area_time_serie
from .models import target_area_daily_time_serie

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

def catalogo_localita(request):

    aree_di_interesse = target_area_input_data.objects.all().order_by('id')
    # from target_area_input_data select *, order by id

    context_dict =  {'aree_di_interesse':aree_di_interesse}

    return render(request, 'catalogo_localita.html', context_dict)


def valori_realtime(request):
    
    #  ranna il processing senza rendere niente in una variabile
    get_realtime_pm()

    # va a prendere i dati nei modelli
    aree_di_interesse = target_area_input_data.objects.all()    
    n_aree_di_interesse = target_area_input_data.objects.all().count()    

    record_sensori = target_area_realtime_data.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }

    return render(request, 'valori_realtime.html', context_dict)


@staff_member_required
def valori_realtime_forced_to_history(request):
    

    #  ranna il processing senza rendere niente in una variabile
    get_realtime_and_save_history_pm()

    # va a prendere i dati nei modelli
    aree_di_interesse = target_area_input_data.objects.all()    
    n_aree_di_interesse = target_area_input_data.objects.all().count()    

    record_sensori = target_area_realtime_data.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }

    return render(request, 'valori_realtime_forced_to_history.html', context_dict)



# solo raffigurazione
def serie_storiche(request):

    print("Richiamo dati in target_area_time_serie...")
    dataset_dei_grafici = target_area_time_serie.objects.all()
    print("Dati in target_area_time_serie acquisiti!")

    context_dict={
        "dataset_dei_grafici":dataset_dei_grafici
                }

    return render(request, 'serie_storiche.html', context_dict)





# solo raffigurazione
def serie_storiche_giornaliere(request):

    print("Richiamo dati in target_area_daily_time_serie...")
    dataset_dei_grafici = target_area_daily_time_serie.objects.all()
    print("Dati in target_area_daily_time_serie acquisiti!")

    context_dict={
        "dataset_dei_grafici":dataset_dei_grafici
                }

    return render(request, 'serie_storiche_giornaliere.html', context_dict)