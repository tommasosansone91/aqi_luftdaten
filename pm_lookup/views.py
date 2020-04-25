from django.shortcuts import render
import numpy as np

from . import processing
from . import processing_2

from .processing import get_pm
from .processing_2 import get_pm_2

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
    
    context_dict = get_pm_2()


    return render(request, 'valori_particolato.html', context_dict)


