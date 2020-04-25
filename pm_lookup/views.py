from django.shortcuts import render
import numpy as np

from . import processing
from . import processing_2

from .processing import get_pm
from .processing_2 import get_pm_2

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


