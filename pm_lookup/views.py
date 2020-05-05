from django.shortcuts import render
import numpy as np

from pm_lookup.processing.single_location_processing import get_single_location_pm
from pm_lookup.processing.realtime_processing import get_realtime_pm

# provvisorio
from pm_lookup.processing.realtime_plus_history_processing import get_realtime_and_save_history_pm



from .models import target_area_input_data
from .models import target_area_output_data
from .models import target_area_output_data


# Create your views here.

# ogni volta che un user va su un sito e clicca su un url sta facendo una request

def home(request):
    return render(request, 'home.html', {})

# def about(request):
#     return render(request, 'about.html', {})

def particolato_milano(request):
    
    context_dict = get_single_location_pm()

    return render(request, 'particolato_milano.html', context_dict)


def valori_recenti(request):
    

    #  ranna il processing prendendo i cmmon result in una variabile
    # common_output = get_realtime_and_save_history_pm()

    #  ranna il processing senza rendere niente in una variabile
    get_realtime_and_save_history_pm()

    # va a prendere i dati nei modelli
    aree_di_interesse = target_area_input_data.objects.all()    
    n_aree_di_interesse = target_area_input_data.objects.all().count()    

    record_sensori = target_area_output_data.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }


    return render(request, 'valori_recenti.html', context_dict)


def serie_storiche(request):

    import numpy as np
    import matplotlib.pyplot as plt

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)

    # sono liste
    nse1 = np.random.randn(len(t))                 # white noise 1
    nse2 = np.random.randn(len(t))          
    
    print(nse1)       # white noise 2

    # Two signals with a coherent part at 10Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)

    # sono liste
    print(cxy)
    print(f)

    axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()

    context_dict={}

    return render(request, 'serie_storiche.html', context_dict)