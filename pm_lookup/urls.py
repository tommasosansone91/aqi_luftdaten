from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('about.html', views.about, name="about"),
    path('valori_particolato', views.valori_particolato, name="valori_particolato"),
    path('particolato_milano', views.particolato_milano, name="particolato_milano"),
    path('serie_storiche', views.serie_storiche, name="serie_storiche"),
]