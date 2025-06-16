
import traceback
import numpy as np
from django.utils import timezone

# do not import models here as it would raise circular import

# importo i drawers
from pm_lookup.drawers.drawers_1 import draw_timeserie_pollutant_graph

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.utils.time_converters import fix_timezone_mismatch_in_array_of_datetimes

from pm_lookup.processing.utils.air_quality_evaluators import evaluate_pollutant_concentration
from pm_lookup.processing.utils.graphs_drawing_helpers import return_graph_title

from pm_lookup.configs.pollutants_data import POLLUTANTS_DATA

from asgiref.sync import sync_to_async


@sync_to_async
def content_of_generate_series_and_draw_graphs():

    try:
        print("content_of_generate_series_and_draw_graphs - S") 

        from pm_lookup.models import ComputedSerie, SerieParametersSet, HistoricalDatapoint
        # This way, the function is only imported after Django has fully loaded the models 
        # — avoiding the circular reference during the initial import phase

        ComputedSerie.objects.all().delete()

        print("Eliminate tutte le serie storiche in ComputedSerie!")

        print("Inizio generazione serie di dati ed elementi del grafico per ogni set di parametri definito...")

        sets_of_serie_parameters = SerieParametersSet.objects.all()


        for set_osp in sets_of_serie_parameters:

            # filter the historical datapoints based on the place and time horizon
            #---------------------------------------------------------------------

            area_di_interesse = set_osp.area_parameters_set
            aggregation_window_duration = set_osp.aggregation_period
            time_horizon = set_osp.time_horizon

            end_time = timezone.now()
            start_time = end_time - time_horizon


            print("Predisposizione dati ed elementi del grafico per la serie storica definita dal set di parametri %s..." % area_di_interesse.name)


            # isola i record di una area di interesse - è cmq un gruppo di oggetti
            # e di un certo periodo di tempo
            records_serie_storica = HistoricalDatapoint.objects.filter(
                area_parameters_set = area_di_interesse,
                # last_update_time__gte = timezone.now() - timedelta(days=n_giorni),
                last_update_time__gte = start_time,
                last_update_time__lte = end_time
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
                    last_update_time__gte = aggregation_window_start_time,
                    last_update_time__lte = aggregation_window_end_time
                )

                if aggregation_window_datapoints:

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
                    PM10_mean_cathegory_label, PM10_mean_cathegory = evaluate_pollutant_concentration("PM10", PM10_mean)
                    PM25_mean_cathegory_label, PM25_mean_cathegory = evaluate_pollutant_concentration("PM25", PM25_mean)

                    
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

                    print("Costruite le statistiche per i campi dei datapoints raccolti nella finestra temporale di estremi ({}, {}) per il set di parametri {}!".format(aggregation_window_start_time, aggregation_window_end_time, set_osp) )

                else:
                    print("Nessun datapoint nella finestra temporale di estremi ({}, {}) per il set di parametri {} .".format(aggregation_window_start_time, aggregation_window_end_time, set_osp) )
                    print("Passo alla finestra temporale successiva")

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

            last_update_time_values = [ dictionary["last_update_time"] for dictionary in list_of_aggregation_window_dicts ]

            # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
            # errore sopraggiunto dopo il reset del db?
            last_update_time_values = fix_timezone_mismatch_in_array_of_datetimes(last_update_time_values)


            # build the y elements
            
            PM10_mean_values = [ dictionary["PM10_mean"] for dictionary in list_of_aggregation_window_dicts ]
            PM25_mean_values = [ dictionary["PM25_mean"] for dictionary in list_of_aggregation_window_dicts ]
            PM10_mean_cathegory_label_values = [ dictionary["PM10_mean_cathegory_label"] for dictionary in list_of_aggregation_window_dicts ]
            PM25_mean_cathegory_label_values = [ dictionary["PM25_mean_cathegory_label"] for dictionary in list_of_aggregation_window_dicts ]
            PM10_mean_cathegory_values = [ dictionary["PM10_mean_cathegory"] for dictionary in list_of_aggregation_window_dicts ]
            PM25_mean_cathegory_values = [ dictionary["PM25_mean_cathegory"] for dictionary in list_of_aggregation_window_dicts ]
            mean_number_of_contributing_sensors_values = [ dictionary["mean_number_of_contributing_sensors"] for dictionary in list_of_aggregation_window_dicts ]


            # turn the lists into arrays, as they are required for the graph

            # time array
            last_update_time_values_array = np.array(last_update_time_values)

            # values
            PM10_values_array = np.array(PM10_mean_values)
            PM25_values_array = np.array(PM25_mean_values)  
            
            # additional data to display in hover template - mandatory use of customdata go.Scatter argument
            # e.g.
            # customdata = np.array(list(zip(extra_info_values_1, extra_info_values_2)))
            
            PM10_customdata = np.array(
                            list(
                                zip(
                                    mean_number_of_contributing_sensors_values,
                                    PM10_mean_cathegory_label_values
                                    )
                                )
            )

            PM25_customdata = np.array(
                            list(
                                zip(
                                    mean_number_of_contributing_sensors_values,
                                    PM25_mean_cathegory_label_values
                                    )
                                )
            )

            


            if PM10_values_array.size == 0:
                graph_PM10="NO DATA"

            else:
                
                # traccio i grafici e ottengo il javascript
                # bring contstants to a graph contats page
                improved_set_of_parameters_title = '"{}" ( {} )'.format(set_osp.title, set_osp.area_parameters_set.name)

                graph_PM10_title = return_graph_title(pollutant_name="PM10", set_of_parameters_title=improved_set_of_parameters_title)
                graph_PM25_title = return_graph_title(pollutant_name="PM2.5", set_of_parameters_title=improved_set_of_parameters_title)

                PM10_air_quality_cathegories_geometries = POLLUTANTS_DATA["PM10"]["air_quality_categories_geometries"]
                PM25_air_quality_cathegories_geometries = POLLUTANTS_DATA["PM25"]["air_quality_categories_geometries"]

                # eventually draw thresholds of concentrations of pollutants

                list_of_aggregation_periods_threshold_values_for_PM10 = [couple[0] for couple in POLLUTANTS_DATA["PM10"]["aggregation_period_vs_pollutant_concentration_thresholds_map"]]
                    
                if aggregation_window_duration in list_of_aggregation_periods_threshold_values_for_PM10:

                    for couple in POLLUTANTS_DATA["PM10"]["aggregation_period_vs_pollutant_concentration_thresholds_map"]:
                        if couple[0] == set_osp.aggregation_period:
                            pollutant_maximum_allowed_concentration_for_aggregation_period = couple[1]

                            PM10_threshold_for_aggregation_period = np.array([pollutant_maximum_allowed_concentration_for_aggregation_period for i in last_update_time_values_array])


                            graph_PM10 = draw_timeserie_pollutant_graph(
                                            time_values=last_update_time_values_array, 
                                            pollutant_values=PM10_values_array, 
                                            pollutant_threshold=PM10_threshold_for_aggregation_period, 
                                            AQ_cathegories_geometries=PM10_air_quality_cathegories_geometries,
                                            graph_title=graph_PM10_title,
                                            pollutant_name=POLLUTANTS_DATA["PM10"]["name"],
                                            pollutant_uom=POLLUTANTS_DATA["PM10"]["unit_of_measure"],
                                            customdata=PM10_customdata
                                        )

                else:
                    graph_PM10 = draw_timeserie_pollutant_graph(
                                    time_values=last_update_time_values_array, 
                                    pollutant_values=PM10_values_array, 
                                    AQ_cathegories_geometries=PM10_air_quality_cathegories_geometries,
                                    graph_title=graph_PM10_title,
                                    pollutant_name=POLLUTANTS_DATA["PM10"]["name"],
                                    pollutant_uom=POLLUTANTS_DATA["PM10"]["unit_of_measure"],
                                    customdata=PM10_customdata,
                                )
            
            if PM25_values_array.size == 0:
                graph_PM25="NO DATA"

            else:  

                list_of_aggregation_periods_threshold_values_for_PM25 = [couple[0] for couple in POLLUTANTS_DATA["PM25"]["aggregation_period_vs_pollutant_concentration_thresholds_map"]]
                
                if aggregation_window_duration in list_of_aggregation_periods_threshold_values_for_PM25:

                    for couple in POLLUTANTS_DATA["PM25"]["aggregation_period_vs_pollutant_concentration_thresholds_map"]:
                        if couple[0] == set_osp.aggregation_period:
                            pollutant_maximum_allowed_concentration_for_aggregation_period = couple[1]

                            PM25_threshold_for_aggregation_period = np.array([pollutant_maximum_allowed_concentration_for_aggregation_period for i in last_update_time_values_array])

                            graph_PM25 = draw_timeserie_pollutant_graph(
                                            time_values=last_update_time_values_array, 
                                            pollutant_values=PM25_values_array, 
                                            AQ_cathegories_geometries=PM25_air_quality_cathegories_geometries,
                                            pollutant_threshold=PM25_threshold_for_aggregation_period, 
                                            graph_title=graph_PM25_title,
                                            pollutant_name=POLLUTANTS_DATA["PM25"]["name"],
                                            pollutant_uom=POLLUTANTS_DATA["PM25"]["unit_of_measure"],
                                            customdata=PM25_customdata,
                                        )

                else:
                    graph_PM25 = draw_timeserie_pollutant_graph(
                                    time_values=last_update_time_values_array, 
                                    pollutant_values=PM25_values_array, 
                                    AQ_cathegories_geometries=PM25_air_quality_cathegories_geometries,
                                    graph_title=graph_PM25_title,
                                    pollutant_name=POLLUTANTS_DATA["PM25"]["name"],
                                    pollutant_uom=POLLUTANTS_DATA["PM25"]["unit_of_measure"],
                                    customdata=PM25_customdata,
                                )


            # save data into ComputedSerie object

            # lists must be stringified

            # try:
            
            new_datapoints_serie_computed_element = ComputedSerie(

                serie_parameters_set = set_osp,

                # questi sono vettori di valori

                # il join deve essere usato sulle liste, non sugli array

                # Convert datetime objects to ISO format strings
                # this is because Object of type datetime is not JSON serializable
                record_time_values = [dt.isoformat() for dt in last_update_time_values], # This should be a list
                
                PM10_mean_values = PM10_mean_values, # This should be a list
                PM25_mean_values = PM25_mean_values, # This should be a list

                number_of_contributing_sensors_values = mean_number_of_contributing_sensors_values, # This should be a list

                PM10_graph_div = graph_PM10,
                PM25_graph_div = graph_PM25

            )

            new_datapoints_serie_computed_element.save()

            # a set of parameters was used as input to create the computed serie+graph

            # except Exception as e:
            #     print(f"Error while saving a new computed serie model object: {e}")
            #     print("printing the complete traceback:\n")
            #     traceback.print_exc()

            print("Predisposti dati ed elementi del grafico per la serie storica per il set dei parametri {}!".format(set_osp) )  

        print("Predisposti dati ed elementi dei grafici per le serie storiche per tutti i set di parametri!") 


    except Exception as e:
        print(f"Error during series generation: {e}")
        print("printing the complete traceback:\n")
        traceback.print_exc()

    print("content_of_generate_series_and_draw_graphs - E")



