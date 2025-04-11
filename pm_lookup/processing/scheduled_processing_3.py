# from datetime import timedelta
# # from datetime import datetime
# from django.utils import timezone

# import numpy as np

# from pm_lookup.models import TargetArea
# from pm_lookup.models import RealtimeDatapoints
# from pm_lookup.models import HistoricalDatapoints
# from pm_lookup.models import DatapointsSerieParameters
# from pm_lookup.models import DatapointsSerieComputed

# # importo i drawers
# from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph
# from pm_lookup.drawers.drawer1 import draw_timeserie_PM25_graph

# # per rivalutare le categorie di qualità dell'aria dei valori di mede orarii
# from .auxiliary_processing import evaluate_PM10, evaluate_PM_in_HistoricalDatapoints_elements
# from .auxiliary_processing import evaluate_PM25

# # per usare la funzione fllor in caso i dati storici orari non siano sufficienti per coprire i n ore di dati medi dichiarati
# import math

# # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# # errore sopraggiunto dopo il reset del db?
# from pm_lookup.processing.auxiliary_processing import fix_timezone_mismatch_1


# def arrange_hourlyaggregated_datapoints_series_and_graphs():

#     DatapointsSerieComputed.objects.all().delete()

#     print("Eliminate tutte le serie storiche orarie in DatapointsSerieComputed!")

#     # print("Inizio disposizione dati in serie storiche orarie per ogni località...")




#     for area_di_interesse in TargetArea.objects.all():

#         print("Predisposizione dati ed elementi del grafico per la serie storica oraria per %s..." % area_di_interesse.name)

#         n_giorni = 30

#         # isola i record di una località - è cmq un gruppo di oggetti
#         # +
#         # prendo i record delle 24 ore degli ultimi 30 giorni
#         records_serie_storica = HistoricalDatapoints.objects.filter(
#             Target_area_input_data = area_di_interesse,
#             Last_update_time__gte = timezone.now() - timedelta(days=n_giorni),
#             Last_update_time__lte = timezone.now()
#         )
        

#         PM10_mean = [i.PM10_mean for i in records_serie_storica]
#         PM25_mean = [i.PM25_mean for i in records_serie_storica]
#         number_of_contributing_sensors = [i.number_of_contributing_sensors for i in records_serie_storica]
#         last_update_time = [ i.last_update_time for i in records_serie_storica]

#         # evaluate pm mean values into cathegories to add them to the series
#         results_dict = evaluate_PM_in_HistoricalDatapoints_elements(records_serie_storica)


#         # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
#         # errore sopraggiunto dopo il reset del db?
#         last_update_time = fix_timezone_mismatch_1(last_update_time)


#         # nota che non ho bsogno di ritrasformare la stringa salvata nel db in numeri, me li legge già come numeri.
#         PM10_hourly_mean = [ round( np.mean( PM10_mean[ 0 + n_ore*i : n_ore + n_ore*i] ) , 2)  for i in range(n_ore) ]
#         PM25_hourly_mean = [ round( np.mean( PM25_mean[ 0 + n_ore*i : n_ore + n_ore*i] ) , 2)  for i in range(n_ore) ]

#         PM10_hourly_mean_cathegory_label = [ evaluate_PM10(i)[0] for i in PM10_hourly_mean ]
#         PM25_hourly_mean_cathegory_label = [ evaluate_PM25(i)[0] for i in PM25_hourly_mean ]

#         PM10_hourly_mean_cathegory = [ evaluate_PM10(i)[1] for i in PM10_hourly_mean ]
#         PM25_hourly_mean_cathegory = [ evaluate_PM25(i)[1] for i in PM25_hourly_mean ]


#         Mean_number_of_contributing_sensors = [ round( np.mean( number_of_contributing_sensors[ 0 + n_ore*i : n_ore + n_ore*i] ) , 2)  for i in range(n_ore) ]

#         Update_date = [ last_update_time[ 0 + n_ore*i ]  for i in range(n_ore) ]
        
#         # le date+ore vengono strippate delle ore, lasciando solo il giorno
#         Update_date = [ element.date() for element in Update_date ]

#         serie_storica = {
#                         #ce n'è solo una perchè l'ho filtrata
#                         "TargetArea" : area_di_interesse.name,

#                         # questi sono vettori di valori

#                         "Update_date" : Update_date,

#                         "PM10_hourly_mean" : PM10_hourly_mean,
#                         "PM25_hourly_mean" : PM25_hourly_mean,

#                         "PM10_hourly_mean_cathegory_label" : PM10_hourly_mean_cathegory_label,
#                         "PM25_hourly_mean_cathegory_label" : PM25_hourly_mean_cathegory_label,

#                         "PM10_hourly_mean_cathegory" : PM10_hourly_mean_cathegory,
#                         "PM25_hourly_mean_cathegory" : PM25_hourly_mean_cathegory,

#                         "Mean_number_of_contributing_sensors" : Mean_number_of_contributing_sensors,

#                         }



        

#         # la posizione di serie storiche indica la città

#         # print(serie_storiche[0].keys())

#         # time array
#         time_values = np.array(serie_storica['Update_date'])

#         # values
#         PM10_values = np.array(serie_storica['PM10_hourly_mean'])
#         PM25_values = np.array(serie_storica['PM25_hourly_mean'])  

#             # colora il retro del grafico per fasce anzchè fare le linee di soglia

#         # a questo script si applicano i limiti normativi orarii

#         # pm10 maxs
#         PM10_hourly_max_35_days_max = np.array([50 for i in time_values])
#         # PM10_annual_mean_max = np.array([40 for i in time_values])

#         #PM2.5 maxs
#         # PM25_annual_mean_max = np.array([20 for i in time_values])

#         # trovare un modo per far comparire nelle etichette del grafico
         
            

#         # traccio i grafici e ottengo il javascript
#         graph_PM10_title = "Serie storiche orarie del PM10 per "+area_di_interesse.name
#         graph_PM25_title = "Serie storiche orarie del PM2.5 per "+area_di_interesse.name

#         graph_PM10 = draw_timeserie_PM10_graph(time_values, PM10_values, PM10_hourly_max_35_days_max=PM10_hourly_max_35_days_max, graph_title=graph_PM10_title)
#         graph_PM25 = draw_timeserie_PM25_graph(time_values, PM25_values, graph_title=graph_PM25_title)

        

#         elementi_grafico = DatapointsSerieComputed(
#                                                     # errore qui
#                                                     Datapoints_serie_parameters = DatapointsSerieParameters.objects.get(TargetArea=area_di_interesse),

#                                                     # questi sono vettori di valori

#                                                     record_time_values = '[' + ', '.join(str(e) for e in  serie_storica['Update_date'] ) +']',

#                                                     PM10_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM10_hourly_mean'] ) +']',
#                                                     PM25_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM25_hourly_mean'] ) +']',

#                                                     PM10_mean_cathegory_label_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_hourly_mean_cathegory_label'] ) +'"]',
#                                                     PM25_mean_cathegory_label_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_hourly_mean_cathegory_label'] ) +'"]',

#                                                     PM10_mean_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_hourly_mean_cathegory'] ) +'"]',
#                                                     PM25_mean_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_hourly_mean_cathegory'] ) +'"]',

#                                                     number_of_contributing_sensors_values = '[' + ', '.join(str(e) for e in  serie_storica['Mean_number_of_contributing_sensors'] ) +']',

#                                                     PM10_graph_div = graph_PM10,
#                                                     PM25_graph_div = graph_PM25,

#                                                     )

#         elementi_grafico.save()

#         print("Predisposti dati ed elementi del grafico per la serie storica oraria per %s!" % area_di_interesse.name)  

#     print("Predisposti dati ed elementi dei grafici per le serie storiche orarie per tutte le località!")  