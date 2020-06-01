from django.shortcuts import render
import numpy as np

from pm_lookup.processing.single_location_processing import get_single_location_pm
from pm_lookup.processing.realtime_processing import get_realtime_pm
from pm_lookup.processing.realtime_plus_history_processing import get_realtime_and_save_history_pm

from .models import target_area_input_data
from .models import target_area_output_data
from .models import target_area_history_data

from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

# ogni volta che un user va su un sito e clicca su un url sta facendo una request

def home(request):
    return render(request, 'home.html', {})

def catalogo_api(request):
    return render(request, 'catalogo_api.html', {})

# def about(request):
#     return render(request, 'about.html', {})

# def particolato_milano(request):
    
#     context_dict = get_single_location_pm()

#     return render(request, 'particolato_milano.html', context_dict)


def valori_realtime(request):
    
    #  ranna il processing senza rendere niente in una variabile
    get_realtime_pm()

    # va a prendere i dati nei modelli
    aree_di_interesse = target_area_input_data.objects.all()    
    n_aree_di_interesse = target_area_input_data.objects.all().count()    

    record_sensori = target_area_output_data.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }

    return render(request, 'valori_realtime.html', context_dict)


@staff_member_required
def valori_realtime_forced_to_history(request):
    

    #  ranna il processing senza rendere niente in una variabile
    get_realtime_and_save_history_pm()

    # va a prendere i dati nei modelli
    aree_di_interesse = target_area_input_data.objects.all()    
    n_aree_di_interesse = target_area_input_data.objects.all().count()    

    record_sensori = target_area_output_data.objects.all()

    context_dict = {
                    'aree_di_interesse':aree_di_interesse,
                    'n_aree_di_interesse':n_aree_di_interesse,
                    # 'common_output':common_output,
                    'record_sensori':record_sensori
                    }

    return render(request, 'valori_realtime_forced_to_history.html', context_dict)


import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go


# solo raffigurazione
def serie_storiche(request):

    print("Inizio disposizione dati storici in una serie storica per ogni località...")

    serie_storiche = []

    for area_di_interesse in target_area_input_data.objects.all():
        
        # isola i record di una località - è cmq un gruppo di oggetti
        records_serie_storica = target_area_history_data.objects.filter(Target_area_input_data=area_di_interesse)
        
        # prendo i record delle 24 ore degli ultimi 30 giorni
        Lunghezza_temporale = 24*30

        records_serie_storica = records_serie_storica[: Lunghezza_temporale - 1]

        # nota: i dati sno già ordinati per default in ordine decrescente

        serie_storica = {
                        #ce n'è solo una perchè l'ho filtrata
                        "Target_area_input_data" : area_di_interesse.Name,

                        # questi sono vettori di valori

                        "Last_update_time" : [i.Last_update_time for i in records_serie_storica],

                        "PM10_mean" : [i.PM10_mean for i in records_serie_storica],
                        "PM25_mean" : [i.PM25_mean for i in records_serie_storica],

                        "PM10_quality" : [i.PM10_quality for i in records_serie_storica],
                        "PM25_quality" : [i.PM25_quality for i in records_serie_storica],

                        "PM10_cathegory" : [i.PM10_cathegory for i in records_serie_storica],
                        "PM25_cathegory" : [i.PM25_cathegory for i in records_serie_storica],

                        "n_selected_sensors" : [i.n_selected_sensors for i in records_serie_storica],

                        }

        # print(serie_storica)

        serie_storiche.append(serie_storica)
        print("Predisposti dati per %s" % area_di_interesse.Name)

    # la posizione di serie storiche indica la città

    # print(serie_storiche[0].keys())

    # time array
    x_values = np.array(serie_storiche[0]['Last_update_time'])

    # values
    PM10_values = np.array(serie_storiche[0]['PM10_mean'])
    PM25_values = np.array(serie_storiche[0]['PM25_mean'])

    # pm10 maxs
    PM10_daily_max_35_days_max = np.array([50 for i in x_values])
    PM10_annual_mean_max = np.array([40 for i in x_values])

    #PM2.5 maxs
    PM25_annual_mean_max = np.array([20 for i in x_values])

    PM10_line = go.Scatter(
                    x=x_values, 
                    y=PM10_values,
                    mode='lines',
                    name="PM 10 [µg/m³]", 

                    marker=dict(
                                color='rgb(128,128,128)',
                                )                    
                    )


    PM10_daily_max_35_days_max_line = go.Scatter(
                                            x=x_values, 
                                            y=PM10_daily_max_35_days_max,
                                            mode='lines',
                                            name="Soglia massima per la concentrazione giornaliera del PM10", 
                                            
                                            marker=dict(
                                                        # size=12,
                                                        color='rgb(255,0,0)',
                                                        # symbol='pentagon',
                                                        # line = {'width':2}    
                                                        )

                                            )
    # ha senso rappresentarla?
    PM10_annual_mean_max_line = go.Scatter(
                    x=x_values, 
                    y=PM10_annual_mean_max,
                    mode='lines',
                    name="Soglia massima per la concentrazione media annuale del PM10", 
                    
                    marker=dict(
                                # size=12,
                                color='rgb(220,20,60)',
                                # symbol='pentagon',
                                # line = {'width':2}    
                                )

                    )                  

# ----------------------------------------------

    PM25_line = go.Scatter(
                x=x_values, 
                y=PM25_values,
                mode='lines',
                name="PM 2.5 [µg/m³]", 

                marker=dict(
                            color='rgb(105,105,105)',
                            )
                )  

        # ha senso rappresentarla?
    PM25_annual_mean_max_line = go.Scatter(
                    x=x_values, 
                    y=PM25_annual_mean_max,
                    mode='lines',
                    name="Soglia massima per la concentrazione media annuale del PM2.5", 
                    
                    marker=dict(
                                # size=12,
                                color='rgb(0,206,209)',
                                # symbol='pentagon',
                                # line = {'width':2}    
                                )
                )


    data=[ PM10_line, PM10_annual_mean_max_line, PM10_daily_max_35_days_max_line,  ]

    # PM25_line, PM25_annual_mean_max_line

    layout=go.Layout(title="Line Charts")

    fig=go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename="My line plot.html")


# ---


    context_dict={}

    return render(request, 'serie_storiche.html', context_dict)


