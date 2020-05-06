from django.urls import path
from . import views # nota che con questo importo tutte le liste
from . import views_api # devo aggiungerlo perchè ho delle altre views

urlpatterns = [
    path('', views.home, name="home"),
    # path('about.html', views.about, name="about"),
    path('valori_recenti', views.valori_recenti, name="valori_recenti"),
    path('particolato_milano', views.particolato_milano, name="particolato_milano"),
    path('serie_storiche', views.serie_storiche, name="serie_storiche"),

    # viste delle api

    # generalmente si fa una app per le api 
    # e poi si mette include negli urls globali di progetto gli urls dell'app api preceduti dal pattern api/

    # api liste

    # poichè ho messo la sua views in un altro py, devo metterne il nome prima della funzione di views
    path('api/cities_list', views_api.cities_list_api, name="cities_list"),
    path('api/historical_data', views_api.historical_data_api, name="historical_data"),
    path('api/realtime_data', views_api.realtime_data_api, name="realtime_data"),

    # api di dettaglio, quindi devo passare in ingresso (URL) il parametro

    path('api/city_detail/<int:pk>', views_api.city_detail_api, name="city_detail"),


    # mantieni lo standard di nomenclatura tra i tre termini
]