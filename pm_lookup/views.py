from django.shortcuts import render
import numpy as np

from . import processing
from . import processing_2

from .processing import get_pm
from .processing_2 import get_pm_2
from .processing_2 import save_in_history

from .models import target_area_input_data, target_area_output_data

# Create your views here.

# ogni volta che un user va su un sito e clicca su un url sta facendo una request

def home(request):
    return render(request, 'home.html', {})

# def about(request):
#     return render(request, 'about.html', {})

def particolato_milano(request):
    
    context_dict = get_pm()

    return render(request, 'particolato_milano.html', context_dict)


def valori_particolato(request):
    
    common_output = get_pm_2()



    aree_di_interesse = target_area_input_data.objects.all()    
    n_aree_di_interesse = target_area_input_data.objects.all().count()    

    record_sensori = target_area_output_data.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    'common_output':common_output,
                    'record_sensori':record_sensori
                    }


    return render(request, 'valori_particolato.html', context_dict)


def serie_storiche(request):

    import numpy as np
    import matplotlib.pyplot as plt

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))                 # white noise 1
    nse2 = np.random.randn(len(t))                 # white noise 2

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
    axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()

    context_dict={}

    return render(request, 'serie_storiche.html', context_dict)