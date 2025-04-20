from datetime import timedelta
# from datetime import datetime
from django.utils import timezone

import numpy as np

from pm_lookup.models import TargetArea
from pm_lookup.models import HistoricalDatapoints
from pm_lookup.models import DatapointsSerieParameters
from pm_lookup.models import DatapointsSerieComputed

# importo i drawers
from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph, draw_timeserie_PM25_graph

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.utils.time_converters import fix_timezone_mismatch_in_array_of_datetimes

from pm_lookup.processing.utils.air_quality_evaluators import evaluate_PM10, evaluate_PM25, evaluate_PM_in_HistoricalDatapoints_elements


# this function must parse all the datapointsserieparameters 
# and build the correspondant serie for each of them.


def arrange_datapoints_series_and_graphs():

    DatapointsSerieComputed.objects.all().delete()

    print("Eliminate tutte le serie storiche in DatapointsSerieComputed!")

    print("Inizio disposizione dati ed elementi del grafico per ogni set di parametri definito...")

    sets_of_serie_parameters = DatapointsSerieParameters.objects.all()


    for set_osp in sets_of_serie_parameters:

        # filter the historical datapoints based on the place and time horizon
        #---------------------------------------------------------------------

        print("Predisposizione dati ed elementi del grafico per la serie storica definita dal set di parametri %s..." % area_di_interesse.name)

        area_di_interesse = set_osp.target_area
        start_time = set_osp.start_time
        end_time = set_osp.end_time
        time_horizon = end_time - start_time
        aggregation_window_duration = set_osp.aggregation_period


        # isola i record di una località - è cmq un gruppo di oggetti
        # e di un certo periodo di tempo
        records_serie_storica = HistoricalDatapoints.objects.filter(
            Target_area_input_data = area_di_interesse,
            # Last_update_time__gte = timezone.now() - timedelta(days=n_giorni),
            Last_update_time__gte = start_time,
            Last_update_time__lte = end_time
        )


        # cycle over the time horizon,
        # start by aggregation_window_start_time = start_time
        # stop when aggregation_window_end_time >= end_time

        list_of_aggregation_window_dicts = list()

        aggregation_window_start_time = start_time
        aggregation_window_end_time = start_time + aggregation_window_duration 

        while True:  
        # do-while
        # in this way, the cycle will always run at least one time

            aggregation_window_datapoints = records_serie_storica.filter(
                Last_update_time__gte = aggregation_window_start_time,
                Last_update_time__lte = aggregation_window_end_time
            )


            # evaluate pm mean values into cathegories to add them to the series
            results_dict = evaluate_PM_in_HistoricalDatapoints_elements(aggregation_window_datapoints)

            # apply statistics to aggregation_window_datapoints

            list_of_last_update_time_of_aggregation_window_datapoints = [i.last_update_time for i in aggregation_window_datapoints]
            
            list_of_PM10_values_of_aggregation_window_datapoints = [i.PM10_mean for i in aggregation_window_datapoints]
            list_of_PM25_values_of_aggregation_window_datapoints = [i.PM25_mean for i in aggregation_window_datapoints]
            
            list_of_number_of_contributing_sensors_of_aggregation_window_datapoints = [i.number_of_contributing_sensors for i in aggregation_window_datapoints]

            # the update time for the single datapoint fo the serie will be the oldest of the group of aggregated datapoints
            oldest_record_time_of_aggregation_window_datapoints = min(list_of_last_update_time_of_aggregation_window_datapoints)

            # this time i also have to build a stathistic for the number of contributing sensor: int mean
            array_of_number_of_contributing_sensors = np.array(list_of_number_of_contributing_sensors_of_aggregation_window_datapoints)
            array_of_number_of_contributing_sensors = array_of_number_of_contributing_sensors.astype(int)
            mean_number_of_contributing_sensors = int(round(np.mean(array_of_number_of_contributing_sensors)))

            PM10_array = np.array(list_of_PM10_values_of_aggregation_window_datapoints)
            PM10_array = PM10_array.astype(float)
            PM10_mean = round(np.mean(PM10_array), 2)

            PM25_array = np.array(list_of_PM25_values_of_aggregation_window_datapoints)
            PM25_array = PM25_array.astype(float)
            PM25_mean = round(np.mean(PM25_array), 2)

            # evaluating the air quality for the means of pollutants
            PM10_mean_cathegory_label, PM10_mean_cathegory = evaluate_PM10(PM10_mean)
            PM25_mean_cathegory_label, PM25_mean_cathegory = evaluate_PM25(PM25_mean)

            
            aggregation_window_dict = {

                "last_update_time" : oldest_record_time_of_aggregation_window_datapoints,

                "PM10_mean" : PM10_mean,
                "PM25_mean" : PM25_mean,

                "PM10_mean_cathegory_label" : PM10_mean_cathegory_label,
                "PM25_mean_cathegory_label" : PM25_mean_cathegory_label,

                "PM10_mean_cathegory" : PM10_mean_cathegory,
                "PM25_mean_cathegory" : PM25_mean_cathegory,

                "mean_number_of_contributing_sensors" : mean_number_of_contributing_sensors,

            }

            # add the dictionary to the list
            list_of_aggregation_window_dicts.append(aggregation_window_dict)

            print("Costruite le statistiche per i campi dei datapoints raccolti nella finestra temporale di estremi ({}, {}) per il set di parametri {}!".format("","", set_osp) )

            # termination condition for do-while
            if aggregation_window_end_time >= end_time:
                break
            else:
                # shift the window forward
                aggregation_window_start_time = aggregation_window_start_time + aggregation_window_duration
                aggregation_window_end_time = aggregation_window_end_time + aggregation_window_duration


        print("Costruite le statistiche per i campi dei datapoints in tutte le finestre temporali per il set di parametri {}!".format(set_osp) )

        
        # use the data inside the list of dicts to build the graphs
        #-----------------------------------------------------------

        # build the t elements

        last_update_time_values = [ i.last_update_time for i in list_of_aggregation_window_dicts ]

        # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
        # errore sopraggiunto dopo il reset del db?
        last_update_time_values = fix_timezone_mismatch_in_array_of_datetimes(last_update_time_values)


        # build the y elements
        
        PM10_mean_values = [ i.PM10_mean for i in list_of_aggregation_window_dicts ]
        PM25_mean_values = [ i.PM25_mean for i in list_of_aggregation_window_dicts ]
        PM10_mean_cathegory_label_values = [ i.PM10_mean_cathegory_label for i in list_of_aggregation_window_dicts ]
        PM25_mean_cathegory_label_values = [ i.PM25_mean_cathegory_label for i in list_of_aggregation_window_dicts ]
        PM10_mean_cathegory_values = [ i.PM10_mean_cathegory for i in list_of_aggregation_window_dicts ]
        PM25_mean_cathegory_values = [ i.PM25_mean_cathegory for i in list_of_aggregation_window_dicts ]
        mean_number_of_contributing_sensors_values = [ i.mean_number_of_contributing_sensors for i in list_of_aggregation_window_dicts ]


        # turn the lists into arrays, as they are required for the graph

        # time array
        last_update_time_values_array = np.array(last_update_time_values)

        # values
        PM10_values_array = np.array(PM10_mean_values)
        PM25_values_array = np.array(PM25_mean_values)  

        # introdurre i limiti solo se aggregation period = 1 day
        # recupera logica da commmit delle serie giornaliere

        # colora il retro del grafico per fasce anzichè fare le linee di soglia

        # questo script è orario, non servono i limiti normativi
        
        # pm10 maxs
        # PM10_daily_max_35_days_max = np.array([50 for i in time_values])
        # PM10_annual_mean_max = np.array([40 for i in time_values])

        #PM2.5 maxs
        # PM25_annual_mean_max = np.array([20 for i in time_values])

        # trovare un modo per far comparire nelle etichette del grafico
        
            

        # traccio i grafici e ottengo il javascript
        # bring contstants to a graph contats page
        graph_PM10_title = "Serie storiche orarie del PM10 per {}".format(set_osp.title)
        graph_PM25_title = "Serie storiche orarie del PM2.5 per {}".format(set_osp.title)

        graph_PM10 = draw_timeserie_PM10_graph(last_update_time_values_array, PM10_values_array, graph_title=graph_PM10_title)
        graph_PM25 = draw_timeserie_PM25_graph(last_update_time_values_array, PM25_values_array, graph_title=graph_PM25_title)

        # save data into DatapointsSerieComputed object

        # lists must be stringified
        
        new_datapoints_serie_computed_element = DatapointsSerieComputed(

            datapoints_serie_parameters = set_osp,

            # questi sono vettori di valori

            # il join deve essere usato sulle liste, non sugli array

            record_time_values = '[' + ', '.join(str(e) for e in  last_update_time_values ) +']',

            PM10_mean_values = '[' + ', '.join(str(e) for e in  PM10_mean_values ) +']',
            PM25_mean_values = '[' + ', '.join(str(e) for e in  PM25_mean_values ) +']',

            PM10_mean_cathegory_label_values = '["' + '", "'.join(str(e) for e in  PM10_mean_cathegory_label_values ) +'"]',
            PM25_mean_cathegory_label_values = '["' + '", "'.join(str(e) for e in  PM25_mean_cathegory_label_values ) +'"]',

            PM10_mean_cathegory_values = '["' + '", "'.join(str(e) for e in  PM10_mean_cathegory_values ) +'"]',
            PM25_mean_cathegory_values = '["' + '", "'.join(str(e) for e in  PM25_mean_cathegory_values ) +'"]',

            number_of_contributing_sensors_values = '[' + ', '.join(str(e) for e in  mean_number_of_contributing_sensors_values ) +']',

            PM10_graph_div = graph_PM10,
            PM25_graph_div = graph_PM25,

        )

        new_datapoints_serie_computed_element.save()

        # a set of parameters was used as input to create the computed serie+graph


        print("Predisposti dati ed elementi del grafico per la serie storica per il set dei parametri {}!".format("") )  

    print("Predisposti dati ed elementi dei grafici per le serie storiche per tutti i set di paraametri!")  
