# from .models import target_area_input_data
# from .models import target_area_output_data
# from .models import target_area_history_data

# # importo i drawers
# from pm_lookup.drawers.drawer1 import draw_historical_PM10_graph
# from pm_lookup.drawers.drawer1 import draw_historical_PM25_graph


# def arrange_time_series_and_graphs(request):

#     print("Inizio disposizione dati in serie storiche per ogni località...")

#     elementi_grafici = []

#     for area_di_interesse in target_area_input_data.objects.all():

#         # isola i record di una località - è cmq un gruppo di oggetti
#         records_serie_storica = target_area_history_data.objects.filter(Target_area_input_data=area_di_interesse)
        
#         # prendo i record delle 24 ore degli ultimi 30 giorni
#         Lunghezza_temporale = 24*30

#         records_serie_storica = records_serie_storica[: Lunghezza_temporale - 1]

#         # nota: i dati sno già ordinati per default in ordine decrescente

#         serie_storica = {
#                         #ce n'è solo una perchè l'ho filtrata
#                         "Target_area_input_data" : area_di_interesse.Name,

#                         # questi sono vettori di valori

#                         "Last_update_time" : [i.Last_update_time for i in records_serie_storica],

#                         "PM10_mean" : [i.PM10_mean for i in records_serie_storica],
#                         "PM25_mean" : [i.PM25_mean for i in records_serie_storica],

#                         "PM10_quality" : [i.PM10_quality for i in records_serie_storica],
#                         "PM25_quality" : [i.PM25_quality for i in records_serie_storica],

#                         "PM10_cathegory" : [i.PM10_cathegory for i in records_serie_storica],
#                         "PM25_cathegory" : [i.PM25_cathegory for i in records_serie_storica],

#                         "n_selected_sensors" : [i.n_selected_sensors for i in records_serie_storica],

#                         }

#         # print(serie_storica)

#         # serie_storiche.append(serie_storica)
#         print("Predisposti dati storici per %s!" % area_di_interesse.Name)

#         # la posizione di serie storiche indica la città

#         # print(serie_storiche[0].keys())

#         # time array
#         time_values = np.array(serie_storica['Last_update_time'])

#         # values
#         PM10_values = np.array(serie_storica['PM10_mean'])
#         PM25_values = np.array(serie_storica['PM25_mean'])  

#             # colora il retro del grafico per fasce anzchè fare le linee di soglia

#         # pm10 maxs
#         PM10_daily_max_35_days_max = np.array([50 for i in time_values])
#         PM10_annual_mean_max = np.array([40 for i in time_values])

#         #PM2.5 maxs
#         PM25_annual_mean_max = np.array([20 for i in time_values])

#         # trovare un modo per far comparire nelle etichette del grafico
         
            

#         # traccio i grafici e ottengo il javascript
#         graph_PM10 = draw_historical_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max)
#         graph_PM25 = draw_historical_PM25_graph(time_values, PM25_values)


        



#         elementi_grafico = {
#                             "Target_area_input_data" : area_di_interesse.Name,

#                             # questi sono vettori di valori

#                             "Last_update_time" : [i.Last_update_time for i in records_serie_storica],

#                             "PM10_mean" : [i.PM10_mean for i in records_serie_storica],
#                             "PM25_mean" : [i.PM25_mean for i in records_serie_storica],

#                             "PM10_quality" : [i.PM10_quality for i in records_serie_storica],
#                             "PM25_quality" : [i.PM25_quality for i in records_serie_storica],

#                             "PM10_cathegory" : [i.PM10_cathegory for i in records_serie_storica],
#                             "PM25_cathegory" : [i.PM25_cathegory for i in records_serie_storica],

#                             "n_selected_sensors" : [i.n_selected_sensors for i in records_serie_storica],

#                             "graph_PM10":graph_PM10,
#                             "graph_PM25":graph_PM25,
#                             }

#         elementi_grafici.append(elementi_grafico)

#         print("Predisposti elementi del grafico per %s!" % area_di_interesse.Name)  
