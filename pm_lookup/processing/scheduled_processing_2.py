from datetime import timedelta
# from datetime import datetime
from django.utils import timezone

import numpy as np

from pm_lookup.models import TargetArea
from pm_lookup.models import RealtimeDatapoints
from pm_lookup.models import HistoricalDatapoints
from pm_lookup.models import DatapointsSerieParameters
from pm_lookup.models import DatapointsSerieComputed

# importo i drawers
from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph
from pm_lookup.drawers.drawer1 import draw_timeserie_PM25_graph

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.auxiliary_processing import evaluate_PM_in_HistoricalDatapoints_elements, fix_timezone_mismatch_1
from pm_lookup.processing.auxiliary_processing import evaluate_PM10, evaluate_PM25


# this function must parse all the datapointsserieparameters and realize the correspondant serie for each of them.


def arrange_datapoints_series_and_graphs():

    DatapointsSerieComputed.objects.all().delete()

    print("Eliminate tutte le serie storiche in DatapointsSerieComputed!")

    print("Inizio disposizione dati in serie storiche per ogni località...")


    for area_di_interesse in TargetArea.objects.all():

        print("Predisposizione dati ed elementi del grafico per la serie storica per %s..." % area_di_interesse.name)

        # isola i record di una località - è cmq un gruppo di oggetti
        # +
        # prendo i record delle 24 ore degli ultimi 30 giorni
        records_serie_storica = HistoricalDatapoints.objects.filter(
            Target_area_input_data = area_di_interesse,
            Last_update_time__gte = timezone.now() - timedelta(days=n_giorni),
            Last_update_time__lte = timezone.now()
        )

        # nota: i dati sno già ordinati per default in ordine decrescente

        # evaluate pm mean values into cathegories to add them to the series
        results_dict = evaluate_PM_in_HistoricalDatapoints_elements(records_serie_storica)

        

        serie_storica = {
                        #ce n'è solo una perchè l'ho filtrata
                        "TargetArea" : area_di_interesse.name,

                        # questi sono vettori di valori

                        "last_update_time_values" : [i.last_update_time for i in records_serie_storica],

                        "PM10_mean_values" : [i.PM10_mean for i in records_serie_storica],
                        "PM25_mean_values" : [i.PM25_mean for i in records_serie_storica],

                        "PM10_mean_cathegory_label_values" : results_dict["PM10_mean_cathegory_label_records_serie_storica"],
                        "PM25_mean_cathegory_label_values" : results_dict["PM25_mean_cathegory_label_records_serie_storica"],

                        "PM10_mean_cathegory_values" : results_dict["PM10_mean_cathegory_records_serie_storica"],
                        "PM25_mean_cathegory_values" : results_dict["PM25_mean_cathegory_records_serie_storica"],

                        "number_of_contributing_sensors_values" : [i.number_of_contributing_sensors for i in records_serie_storica],

                        }


        # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
        # errore sopraggiunto dopo il reset del db?
        serie_storica["last_update_time_values"] = fix_timezone_mismatch_1(serie_storica["last_update_time_values"])


        # la posizione di serie storiche indica la città

        # print(serie_storiche[0].keys())

        # time array
        time_values = np.array(serie_storica['last_update_time_values'])

        # values
        PM10_values = np.array(serie_storica['PM10_mean_values'])
        PM25_values = np.array(serie_storica['PM25_mean_values'])  

            # colora il retro del grafico per fasce anzchè fare le linee di soglia


        # questo script è orario, non servono i limiti normativi
        
        # pm10 maxs
        # PM10_daily_max_35_days_max = np.array([50 for i in time_values])
        # PM10_annual_mean_max = np.array([40 for i in time_values])

        #PM2.5 maxs
        # PM25_annual_mean_max = np.array([20 for i in time_values])

        # trovare un modo per far comparire nelle etichette del grafico
         
            

        # traccio i grafici e ottengo il javascript
        graph_PM10_title = "Serie storiche orarie del PM10 per "+area_di_interesse.name
        graph_PM25_title = "Serie storiche orarie del PM2.5 per "+area_di_interesse.name

        graph_PM10 = draw_timeserie_PM10_graph(time_values, PM10_values, graph_title=graph_PM10_title)
        graph_PM25 = draw_timeserie_PM25_graph(time_values, PM25_values, graph_title=graph_PM25_title)

        

        elementi_grafico = DatapointsSerieComputed(
                                                    # errore qui
                                                    Datapoints_serie_parameters = DatapointsSerieParameters.objects.get(TargetArea=area_di_interesse),

                                                    # questi sono vettori di valori

                                                    record_time_values = '[' + ', '.join(str(e) for e in  serie_storica['last_update_time_values'] ) +']',

                                                    PM10_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM10_mean_values'] ) +']',
                                                    PM25_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM25_mean_values'] ) +']',

                                                    PM10_mean_cathegory_label_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_mean_cathegory_label_values'] ) +'"]',
                                                    PM25_mean_cathegory_label_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_mean_cathegory_label_values'] ) +'"]',

                                                    PM10_mean_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_mean_cathegory_values'] ) +'"]',
                                                    PM25_mean_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_mean_cathegory_values'] ) +'"]',

                                                    number_of_contributing_sensors_values = '[' + ', '.join(str(e) for e in  serie_storica['number_of_contributing_sensors_values'] ) +']',

                                                    PM10_graph_div = graph_PM10,
                                                    PM25_graph_div = graph_PM25,

                                                    )

        elementi_grafico.save()

        print("Predisposti dati ed elementi del grafico per la serie storica per %s!" % area_di_interesse.name)  

    print("Predisposti dati ed elementi dei grafici per le serie storiche per tutte le località!")  
