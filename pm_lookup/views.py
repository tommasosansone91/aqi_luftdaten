from django.shortcuts import render

from pm_lookup.processing.realtime_processing_1 import get_realtime_pm_values
from pm_lookup.processing.realtime_processing_2 import update_realtime_pm_values_and_save_them_in_history

from .models import TargetArea
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import DatapointsSerie
from .models import DailyAggregatedDatapointsSerie

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

    aree_di_interesse = TargetArea.objects.all().order_by('id')
    # from TargetArea select *, order by id

    context_dict =  {'aree_di_interesse':aree_di_interesse}

    return render(request, 'catalogo_localita.html', context_dict)


def valori_realtime(request):
    
    #  ranna il processing senza rendere niente in una variabile
    get_realtime_pm_values()

    # va a prendere i dati nei modelli
    aree_di_interesse = TargetArea.objects.all()    
    n_aree_di_interesse = TargetArea.objects.all().count()    

    record_sensori = RealtimeDatapoints.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }

    return render(request, 'valori_realtime.html', context_dict)

# disabilitato
# @staff_member_required
# def valori_realtime_forced_to_history(request):
    

#     #  ranna il processing senza rendere niente in una variabile
#     update_realtime_pm_values_and_save_them_in_history()

#     # va a prendere i dati nei modelli
#     aree_di_interesse = TargetArea.objects.all()    
#     n_aree_di_interesse = TargetArea.objects.all().count()    

#     record_sensori = RealtimeDatapoints.objects.all()

#     context_dict = {
#                     'aree_di_interesse':aree_di_interesse,
#                     'n_aree_di_interesse':n_aree_di_interesse,
#                     # 'common_output':common_output,
#                     'record_sensori':record_sensori
#                     }

#     return render(request, 'valori_realtime_forced_to_history.html', context_dict)



# solo raffigurazione
def serie_storiche(request):

    print("Richiamo dati in DatapointsSerie...")
    dataset_dei_grafici = DatapointsSerie.objects.all()
    print("Dati in DatapointsSerie acquisiti!")

    context_dict={
        "dataset_dei_grafici":dataset_dei_grafici
                }

    print("Dati in trasmissione al template!")

    return render(request, 'serie_storiche.html', context_dict)





# solo raffigurazione
def serie_storiche_giornaliere(request):

    print("Richiamo dati in DailyAggregatedDatapointsSerie...")
    dataset_dei_grafici = DailyAggregatedDatapointsSerie.objects.all()
    print("Dati in DailyAggregatedDatapointsSerie acquisiti!")

    context_dict={
        "dataset_dei_grafici":dataset_dei_grafici
                }

    print("Dati in trasmissione al template!")

    return render(request, 'serie_storiche_giornaliere.html', context_dict)