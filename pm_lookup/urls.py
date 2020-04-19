from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('valori_particolato.html', views.valori_particolato, name="valori_particolato"),
]