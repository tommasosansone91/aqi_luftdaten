from django.db import models


from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now

from pm_lookup.configs.constants import COMPUTED_SERIE_META_VERBOSE_NAME, SET_OF_PARAMETERS_OF_SERIE_META_VERBOSE_NAME


import uuid

############

import numpy as np

########## model import

# importo i drawers
from pm_lookup.drawers.drawers_1 import draw_timeserie_pollutant_graph

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.utils.time_converters import fix_timezone_mismatch_in_array_of_datetimes

from pm_lookup.processing.utils.air_quality_evaluators import evaluate_pollutant_concentration
from pm_lookup.processing.utils.graphs_drawing_helpers import return_graph_title

from pm_lookup.configs.pollutants_data import POLLUTANTS_DATA

#############

# Create your models here.
# nota che i modelli sono tutti in minuscolo

# ogni modello django possiede per default
# id = models.AutoField(primary_key=True)


# these are to guaranteee that 
# the default start time and end time are generated differently every time the "create or edit" function are called, 
# and not only when the models module is imported


class AreaParametersSet(models.Model):

    # id = models.AutoField(primary_key=True)

    # Ho reso il nome univoco così sono obbligato a specificare la diversità nel nome se anche cambio 
    # le coordinate del centro o il raggio
    name = models.CharField(
        max_length=256, 
        blank=False, 
        null=False, 
        unique=True,
        help_text="""Set the name for this area."""
    )

    description = models.TextField(null=False, blank=True)

    latitude = models.FloatField(
        null=False, 
        blank=False,
        help_text="""Set the latitude of the center of this area
        <br>
        e.g.<br>
        Y.YY... (WGS84)
        """
    )

    longitude = models.FloatField(
        null=False, 
        blank=False,
        help_text="""Set the longitude of the center of this area 
        <br>
        e.g.<br>
        X.XX... (WGS84)
        """
    )

    radius = models.FloatField(
        null=False, 
        blank=False,
        help_text="""Set the radius [km] that will define the boundary of this area as a circle around the center."""
    )



    def __str__(self):       
        return  "%s [ lat: %s , long: %s - radius: %s km]"  %    (
                                                        self.name, 
                                                        self.latitude, 
                                                        self.longitude, 
                                                        self.radius
                                                        )  

    class Meta:
        ordering = [
            '-radius', 
            'name'
        ]

        unique_together = ('latitude', 'longitude', 'radius')

        verbose_name = "set of parameters of area"  # Nome al singolare
        verbose_name_plural = "sets of parameters of areas"  # Nome al plurale


class RealtimeDatapoint(models.Model):

    area_parameters_set = models.OneToOneField(
        'AreaParametersSet',
        on_delete=models.CASCADE,
        
    )
    
    # name, radius lat e long le prendo dal target area input data (onetoonefield) usando il .name. .radius, ecc
    
    # AreaParametersSet_name = models.ForeignKey(
    #     'AreaParametersSet',
    #     # AreaParametersSet_name = models.ForeignKey('AreaParametersSet', on_delete....)
    #     # vuol dire: in questo campo metti l'id del modello 'AreaParametersSet'
        
    #     # nota che l'attributo è in minuscolo
    #     on_delete=models.CASCADE,
    # )
    # il primo attributo è il modello cui è associato

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    last_update_time = models.DateTimeField(blank=False, null=False, default=timezone.now )

    number_of_contributing_sensors = models.PositiveIntegerField(null=True)

    # these could be switched to a single json

    PM10_mean = models.FloatField(null=False, blank=False)
    PM25_mean = models.FloatField(null=False, blank=False)

    # only the realtime data carries field for air quality cathegory and label, 
    # as it is useful to display its color in the homepage
    PM10_mean_cathegory_label = models.TextField( blank=False, null=False)
    PM25_mean_cathegory_label = models.TextField( blank=False, null=False)

    PM10_mean_cathegory  = models.CharField(max_length=50, blank=False, null=False)
    PM25_mean_cathegory = models.CharField(max_length=50, blank=False, null=False)


    def __str__(self):       
        return  "%s (%s) [ %s ]"  %  (
                                    self.area_parameters_set.name,
                                    self.area_parameters_set.id, 
                                    datetime.strftime(
                                        self.last_update_time, 
                                        "%H:%M:%S %d-%m-%Y"
                                        ) 
                                    )  


    class Meta:
        ordering = [
            '-area_parameters_set__radius', 
            'area_parameters_set__name'
        ]
        # fixato così
        # ordering = ['-area_parameters_set.radius', 'area_parameters_set.name']

        verbose_name = "realtime datapoint"  # Nome al singolare
        verbose_name_plural = "realtime datapoints"  # Nome al plurale


class HistoricalDatapoint(models.Model):

    area_parameters_set = models.ForeignKey(
        'AreaParametersSet',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    last_update_time = models.DateTimeField(blank=False, null=False, default=timezone.now )

    number_of_contributing_sensors = models.PositiveIntegerField(null=True)

    # these could be switched to a single json

    PM10_mean = models.FloatField(null=False, blank=False)
    PM25_mean = models.FloatField(null=False, blank=False)


    def __str__(self):       
        return  "%s (%s) [ %s ]"  %  (
                                    self.area_parameters_set.name, 
                                    self.area_parameters_set.id, 
                                    datetime.strftime(
                                        self.last_update_time, 
                                        "%H:%M:%S %d-%m-%Y"
                                        ) 
                                    )  
        
 
    class Meta:
        ordering = [
            '-last_update_time', 
            '-area_parameters_set__radius', 
            'area_parameters_set__name'
        ]

        unique_together = ('area_parameters_set', 'last_update_time')
        # altrimenti non ha senso salvare un altro record... se è lo stesso
        # metto il try nel momento del salvataggio

        verbose_name = "historical datapoint"  # Nome al singolare
        verbose_name_plural = "historical datapoints"  # Nome al plurale


# --------------------------------

# --------------------------------


class SerieParametersSet(models.Model):

    area_parameters_set = models.ForeignKey(
        'AreaParametersSet',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    title = models.CharField(
        max_length=256, 
        blank=False, 
        null=False,
        help_text="""Set the name for this set of parameters defining a serie."""
        )

    description = models.TextField(null=False, blank=True)

    time_horizon = models.DurationField(
        null=False,
        blank=False,
        default=timedelta(days=1),
        verbose_name="time horizon",
        help_text="""
        Set the time horizon of the serie.<br>
        The start time of the serie will be equal to: now - time_horizon<br>
        The end time will be equal to the current time.<br>
        <br>
        e.g.<br>
        1 hour = 0 01:00:00<br>
        1 day = 1 00:00:00
        """
    )

    
    aggregation_period = models.DurationField(
        null=False, 
        blank=False, 
        default=timedelta(hours=1),
        verbose_name="aggregation period",
        help_text="""Set the aggregation period of historical datapoints.<br>
        <br>
        e.g.<br>
        1 hour = 0 01:00:00<br>
        1 day = 1 00:00:00"""
        )

    show_serie = models.BooleanField( 
        null=False, 
        blank=False, 
        default=True ,
        verbose_name="show serie",
        help_text="Check this to show the series in the dashboard."
        ) 
    
    
    

    # default: create a time serie of 1h aggregation and having a 1-day time horizon

    def model_save_triggered_generate_series_and_draw_graphs(self):

        ############################

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
            
            new_datapoints_serie_computed_element = ComputedSerie(

                serie_parameters_set = set_osp,

                # questi sono vettori di valori

                # il join deve essere usato sulle liste, non sugli array

                record_time_values = '[' + ', '.join(str(e) for e in  last_update_time_values ) +']',

                PM10_mean_values = '[' + ', '.join(str(e) for e in  PM10_mean_values ) +']',
                PM25_mean_values = '[' + ', '.join(str(e) for e in  PM25_mean_values ) +']',

                number_of_contributing_sensors_values = '[' + ', '.join(str(e) for e in  mean_number_of_contributing_sensors_values ) +']',

                PM10_graph_div = graph_PM10,
                PM25_graph_div = graph_PM25

            )

            new_datapoints_serie_computed_element.save()

            # a set of parameters was used as input to create the computed serie+graph


            print("Predisposti dati ed elementi del grafico per la serie storica per il set dei parametri {}!".format(set_osp) )  

        print("Predisposti dati ed elementi dei grafici per le serie storiche per tutti i set di parametri!")  


    ###############
        


    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # First, save the instance

        # Then rebuild series and graphs
        self.model_save_triggered_generate_series_and_draw_graphs()  



    def __str__(self):       
        return  "%s ( %s ) (%s)"  %  ( self.title , self.area_parameters_set.name, SET_OF_PARAMETERS_OF_SERIE_META_VERBOSE_NAME )  
        
 
    class Meta:
        ordering = [
            '-area_parameters_set__radius', 
            'area_parameters_set__name'
        ]

        unique_together = ('area_parameters_set', 'time_horizon', 'aggregation_period')

        verbose_name = SET_OF_PARAMETERS_OF_SERIE_META_VERBOSE_NAME  # Nome al singolare
        verbose_name_plural = "sets of parameters of series"  # Nome al plurale



class ComputedSerie(models.Model):

    # one SerieParametersSet can have only one corresponding ComputedSerie
    serie_parameters_set = models.OneToOneField(
        'SerieParametersSet',
        on_delete=models.CASCADE,
    )
    # il primo attributo è il modello cui è associato

    # postgres non prende array + datetime
    record_time_values = models.TextField( blank=False, null=False) 

    PM10_mean_values = models.TextField( null=False, blank=False)
    PM25_mean_values = models.TextField( null=False, blank=False)

    number_of_contributing_sensors_values = models.TextField(null=True)

    PM10_graph_div = models.TextField()
    PM25_graph_div = models.TextField()



    def __str__(self):       
        return  "%s ( %s ) (%s)"  %  ( self.serie_parameters_set.title , self.serie_parameters_set.area_parameters_set.name, COMPUTED_SERIE_META_VERBOSE_NAME )  
        
 
    class Meta:
        ordering = [
            '-serie_parameters_set__area_parameters_set__radius',
            'serie_parameters_set__area_parameters_set__name'
        ]

        verbose_name = COMPUTED_SERIE_META_VERBOSE_NAME  # Nome al singolare
        verbose_name_plural = "computed series"  # Nome al plurale
