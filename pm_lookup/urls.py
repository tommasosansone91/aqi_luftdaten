from django.urls import path
from . import views # nota che con questo importo tutte le liste
from . import api # devo aggiungerlo perchè ho delle altre views

urlpatterns = [

    # path, vista, nome di richiamo

    # pagine web
    #------------

    path('', views.home, name="home"),

    path('catalogo_api', views.catalogo_api, name="catalogo_api"),
    path('catalogo_aree_interesse', views.catalogo_aree_interesse, name="catalogo_aree_interesse"),
    path('catalogo_set_parametri_definizione_serie_storiche', views.catalogo_set_parametri_definizione_serie_storiche, name="catalogo_set_parametri_definizione_serie_storiche"),
    
    path('valori_realtime', views.valori_realtime, name="valori_realtime"),
    
    path('grafici_serie_storiche', views.grafici_serie_storiche, name="grafici_serie_storiche"),
    

    # api urls
    #############

    # generalmente si fa una app per le api 
    # e poi si mette include negli urls globali di progetto gli urls dell'app api preceduti dal pattern api/

    # api liste
    #-------------

    # poichè ho messo la sua views in un altro py, devo metterne il nome prima della funzione di views
    path('api/areas_list', api.areas_list_api, name="areas_list"),
    path('api/sets_of_parameters_of_series_list', api.sets_of_parameters_of_series_list_api, name="sets_of_parameters_of_series_list"),
    # path('api/realtime_datapoints_list', api.realtime_datapoints_list_api, name="realtime_datapoints"),

  

    # api di dettaglio
    #---------------------

    # quindi devo passare in ingresso (URL) il parametro

    path('api/area_detail/<int:pk>', api.area_detail_api, name="area_detail"),
    path('api/parameters_for_series_detail/<int:pk>', api.parameters_for_serie_detail_api, name="parameters_for_serie_detail"),
    path('api/realtime_datapoints_detail/<int:pk>', api.realtime_datapoint_detail_api, name="realtime_datapoints_detail"),
    path('api/computed_serie_detail/<int:pk>', api.computed_serie_detail_api, name="computed_serie_detail"),

    # non c'è il dettaglio degli history data perchè così prendo un record solo. è inutile.. ho una ok per ogni record.
    # prendere un insieme di record corrisondenti ad una città ... è prendere una serie storica, quindi tanto vale
    # path('api/historical_datapoints_detail/<int:pk>', api.historical_datapoints_detail_api, name="historical_datapoints_detail"),

    # path('api/computed_serie_detail/<int:pk>', api.computed_serie_detail_api, name="computed_serie_detail"),
   

    # api con molti filtri
    #-----------------------

    path('api/historical_datapoints_subset', api.historical_datapoints_subset_api, name="historical_datapoints_subset"),    


    
    # mantieni lo standard di nomenclatura tra i tre termini
]