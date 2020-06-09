from django.urls import path
from . import views # nota che con questo importo tutte le liste
from . import views_api # devo aggiungerlo perchè ho delle altre views

urlpatterns = [

    # path, vista, nome di richiamo

    path('', views.home, name="home"),

    path('catalogo_api', views.catalogo_api, name="catalogo_api"),
    
    path('valori_realtime', views.valori_realtime, name="valori_realtime"),
    # path('particolato_milano', views.particolato_milano, name="particolato_milano"),

    path('valori_realtime_forced_to_history', views.valori_realtime_forced_to_history, name="valori_realtime_forced_to_history"),

    path('serie_storiche', views.serie_storiche, name="serie_storiche"),

    # viste delle api

    # generalmente si fa una app per le api 
    # e poi si mette include negli urls globali di progetto gli urls dell'app api preceduti dal pattern api/

    # api liste

    # poichè ho messo la sua views in un altro py, devo metterne il nome prima della funzione di views
    path('api/cities_list', views_api.cities_list_api, name="cities_list"),
    path('api/realtime_data', views_api.realtime_data_api, name="realtime_data"),
    path('api/historical_data', views_api.historical_data_api, name="historical_data"),    
    path('api/historical_series', views_api.historical_series_api, name="historical_series"),
    

    # api di dettaglio, quindi devo passare in ingresso (URL) il parametro

    path('api/city_detail/<int:pk>', views_api.city_detail_api, name="city_detail"),
    path('api/realtime_data_detail/<int:pk>', views_api.realtime_data_detail_api, name="realtime_data_detail"),
    path('api/historical_data_detail/<int:pk>', views_api.historical_data_detail_api, name="historical_data_detail"),

    
    # mantieni lo standard di nomenclatura tra i tre termini
]