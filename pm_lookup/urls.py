from django.urls import path
from . import views # nota che con questo importo tutte le liste
from . import api # devo aggiungerlo perchè ho delle altre views

urlpatterns = [

    # path, vista, nome di richiamo

    # pagine web
    #------------

    path(
        '', 
        views.home, 
        name="home"
        ),

    path(
        'catalogo_api', 
        views.catalogo_api, 
        name="catalogo_api"
        ),
    path(
        'catalogo_aree_interesse', 
        views.catalogo_aree_interesse, 
        name="catalogo_aree_interesse"
        ),
    path(
        'catalogo_set_parametri_definizione_serie_storiche', 
         views.catalogo_set_parametri_definizione_serie_storiche, 
         name="catalogo_set_parametri_definizione_serie_storiche"
         ),
    
    path(
        'valori_realtime', 
        views.valori_realtime, 
        name="valori_realtime"
        ),
    
    path(
        'grafici_serie_storiche', 
        views.grafici_serie_storiche, 
        name="grafici_serie_storiche"
        ),
    

    # api urls
    #############

    # generalmente si fa una app per le api 
    # e poi si mette include negli urls globali di progetto gli urls dell'app api preceduti dal pattern api/

    # api liste
    #-------------

    # poichè ho messo la sua views in un altro py, devo metterne il nome prima della funzione di views
    path(
        'api/area_parameters_set_list', 
        api.area_parameters_set_getall_api, 
        name="area_parameters_set_list"
        ),
    path(
        'api/serie_parameters_set_list', 
        api.serie_parameters_set_getall_api, 
        name="serie_parameters_set_list"
        ),
    # path('api/realtime_datapoints_list', api.realtime_datapoints_list_api, name="realtime_datapoints"),

  

    # api di dettaglio
    #---------------------

    # quindi devo passare in ingresso (URL) il parametro

    path(
        'api/area_parameters_set/<int:pk>', 
        api.area_parameters_set_getbyid_api, 
        name="area_parameters_set"
        ),
    path(
        'api/serie_parameters_set/<int:pk>', 
        api.serie_parameters_set_getbyid_api, 
        name="serie_parameters_set"
        ),
    path(
        'api/realtime_datapoint/<int:pk>', 
         api.realtime_datapoint_getbyareaparameterssetid_api, 
         name="realtime_datapoint"
         ),
    path(
        'api/computed_serie/<int:pk>', 
        api.computed_serie_getbyserieparameterssetid_api, 
        name="computed_serie"
        ),

    # non c'è il dettaglio degli history data perchè così prendo un record solo. è inutile.. ho una ok per ogni record.
    # prendere un insieme di record corrisondenti ad una città ... è prendere una serie storica, quindi tanto vale
    # path('api/historical_datapoints_detail/<int:pk>', api.historical_datapoints_detail_api, name="historical_datapoints_detail"),

    # path('api/computed_serie/<int:pk>', api.computed_serie_api, name="computed_serie"),
   

    # api con molti filtri
    #-----------------------

    path(
        'api/historical_datapoints_subset', 
        api.historical_datapoint_subset_getbyfilter_api, 
        name="historical_datapoints_subset"
        ),   


    # custom messaging system
    # ------------------------- 

    path(
        'publish_message/', 
        views.publish_message, 
        name='publish_message'
        ),

    path(
        'get_messages/', 
         views.get_messages, 
         name='get_messages'
         ),

    path(
        'show_messages/', 
        views.message_display_page, 
        name='show_messages'
        ),


    
    # mantieni lo standard di nomenclatura tra i tre termini
]