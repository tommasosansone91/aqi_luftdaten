import numpy as np

from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_realtime_data
from pm_lookup.models import target_area_history_data
from pm_lookup.models import target_area_daily_time_serie

# importo i drawers
from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph
from pm_lookup.drawers.drawer1 import draw_timeserie_PM25_graph

# per rivalutare le categorie di qualità dell'aria dei valori di mede giornalieri
from .auxiliary_processing import evaluate_PM10
from .auxiliary_processing import evaluate_PM25


def arrange_daily_time_series_and_graphs():

    target_area_daily_time_serie.objects.all().delete()

    print("Eliminate tutte le serie storiche giornaliere in target_area_daily_time_serie!")

    # print("Inizio disposizione dati in serie storiche giornaliere per ogni località...")

    # prendo i record delle 24 ore degli ultimi 30 giorni
    Lunghezza_temporale = 24*30


    for area_di_interesse in target_area_input_data.objects.all():

        print("Predisposizione dati ed elementi del grafico per la serie storica giornaliera per %s..." % area_di_interesse.Name)

        # isola i record di una località - è cmq un gruppo di oggetti
        records_serie_storica = target_area_history_data.objects.filter(Target_area_input_data=area_di_interesse)
        
        records_serie_storica = records_serie_storica[: Lunghezza_temporale - 1]

        # nota: i dati sno già ordinati per default in ordine decrescente

        # records_serie_storica = [  round( np.mean( records_serie_storica[ 0 + 24*i : 24 + 24*i] ) , 2)  for i in range(30)]

        PM10_mean = [i.PM10_mean for i in records_serie_storica]
        PM25_mean = [i.PM25_mean for i in records_serie_storica]
        n_selected_sensors = [i.n_selected_sensors for i in records_serie_storica]
        Last_update_time = [ i.Last_update_time for i in records_serie_storica]


        PM10_daily_mean = [ round( np.mean( PM10_mean[ 0 + 24*i : 24 + 24*i] ) , 2)  for i in range(30) ]
        PM25_daily_mean = [ round( np.mean( PM25_mean[ 0 + 24*i : 24 + 24*i] ) , 2)  for i in range(30) ]

        PM10_daily_quality = [ evaluate_PM10(i)[0] for i in PM10_daily_mean ]
        PM25_daily_quality = [ evaluate_PM25(i)[0] for i in PM25_daily_mean ]

        PM10_daily_cathegory = [ evaluate_PM10(i)[1] for i in PM10_daily_mean ]
        PM25_daily_cathegory = [ evaluate_PM25(i)[1] for i in PM25_daily_mean ]


        Mean_n_selected_sensors = [ round( np.mean( n_selected_sensors[ 0 + 24*i : 24 + 24*i] ) , 2)  for i in range(30) ]

        Update_date = [ Last_update_time[ 0 + 24*i ]  for i in range(30) ]
        # Update_date = [ i.split()[0] for i in Update_date ]



        serie_storica = {
                        #ce n'è solo una perchè l'ho filtrata
                        "Target_area_input_data" : area_di_interesse.Name,

                        # questi sono vettori di valori

                        "Update_date" : Update_date,

                        "PM10_daily_mean" : PM10_daily_mean,
                        "PM25_daily_mean" : PM25_daily_mean,

                        "PM10_daily_quality" : PM10_daily_quality,
                        "PM25_daily_quality" : PM25_daily_quality,

                        "PM10_daily_cathegory" : PM10_daily_cathegory,
                        "PM25_daily_cathegory" : PM25_daily_cathegory,

                        "Mean_n_selected_sensors" : Mean_n_selected_sensors,

                        }



        

        # la posizione di serie storiche indica la città

        # print(serie_storiche[0].keys())

        # time array
        time_values = np.array(serie_storica['Update_date'])

        # values
        PM10_values = np.array(serie_storica['PM10_daily_mean'])
        PM25_values = np.array(serie_storica['PM25_daily_mean'])  

            # colora il retro del grafico per fasce anzchè fare le linee di soglia

        # pm10 maxs
        PM10_daily_max_35_days_max = np.array([50 for i in time_values])
        PM10_annual_mean_max = np.array([40 for i in time_values])

        #PM2.5 maxs
        PM25_annual_mean_max = np.array([20 for i in time_values])

        # trovare un modo per far comparire nelle etichette del grafico
         
            

        # traccio i grafici e ottengo il javascript
        graph_PM10 = draw_timeserie_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max)
        graph_PM25 = draw_timeserie_PM25_graph(time_values, PM25_values)

        

        elementi_grafico = target_area_daily_time_serie(
                                                    # errore qui
                                                    Target_area_input_data = target_area_input_data.objects.get(Name=area_di_interesse.Name),

                                                    # questi sono vettori di valori

                                                    Record_time_values = '[' + ', '.join(str(e) for e in  serie_storica['Update_date'] ) +']',

                                                    PM10_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM10_daily_mean'] ) +']',
                                                    PM25_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM25_daily_mean'] ) +']',

                                                    PM10_quality_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_daily_quality'] ) +'"]',
                                                    PM25_quality_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_daily_quality'] ) +'"]',

                                                    PM10_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_daily_cathegory'] ) +'"]',
                                                    PM25_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_daily_cathegory'] ) +'"]',

                                                    n_selected_sensors_values = '[' + ', '.join(str(e) for e in  serie_storica['Mean_n_selected_sensors'] ) +']',

                                                    PM10_graph_div = graph_PM10,
                                                    PM25_graph_div = graph_PM25,

                                                    )

        elementi_grafico.save()

        print("Predisposti dati ed elementi del grafico per la serie storica giornaliera per %s!" % area_di_interesse.Name)  
