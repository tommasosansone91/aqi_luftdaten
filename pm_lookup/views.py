from django.shortcuts import render
import numpy as np

from . import processing
from .processing import get_pm

# Create your views here.

# ogni volta che un user va su un sito e clicca su un url sta facendo una request

def home(request):
    return render(request, 'home.html', {})

# def about(request):
#     return render(request, 'about.html', {})

def valori_particolato(request):
    
    context_dict = get_pm()

    return render(request, 'valori_particolato.html', context_dict)