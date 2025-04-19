from django.db import models

from django.utils import timezone
from datetime import datetime
from datetime import timedelta

import uuid


# Create your models here.
# nota che i modelli sono tutti in minuscolo

# ogni modello django possiede per default
# id = models.AutoField(primary_key=True)

class TargetArea(models.Model):

    # id = models.AutoField(primary_key=True)

    # Ho reso il nome univoco così sono obbligato a specificare la diversità nel nome se anche cambio 
    # le coordinate del centro o il raggio
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    description = models.TextField(null=False, blank=True)

    latitude = models.FloatField(null=False, blank=False)

    longitude = models.FloatField(null=False, blank=False)

    radius = models.FloatField(null=False, blank=False)
    # deve essere integer


    def __str__(self):       
        return  "%s --- [ lat: %s , long: %s - radius: %s km]"  %    (
                                                        self.name, 
                                                        self.latitude, 
                                                        self.longitude, 
                                                        self.radius
                                                        )  

    class Meta:
        ordering = ['-radius', 'name']

        unique_together = ('latitude', 'longitude', 'radius')




class RealtimeDatapoints(models.Model):

    # nota che è maiuscolo
    target_area = models.OneToOneField(
        'TargetArea',
        on_delete=models.CASCADE,
        
    )
    
    # name, radius lat e long le prendo dal target area input data (onetoonefield) usando il .name. .radius, ecc
    
    # TargetArea_name = models.ForeignKey(
    #     'TargetArea',
    #     # TargetArea_name = models.ForeignKey('TargetArea', on_delete....)
    #     # vuol dire: in questo campo metti l'id del modello 'TargetArea'
        
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
        return  "%s --- [ %s ]"  %  (
                                    self.target_area.name, 
                                    datetime.strftime(
                                        self.last_update_time, 
                                        "%H:%M:%S %d-%m-%Y"
                                        ) 
                                    )  


    class Meta:
        ordering = ['-target_area__radius', 'target_area__name']
        # fixato così
        # ordering = ['-target_area.radius', 'target_area.name']

        verbose_name = "realtime datapoint"  # Nome al singolare
        verbose_name_plural = "realtime datapoints"  # Nome al plurale


class HistoricalDatapoints(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'TargetArea',
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
        return  "%s --- [ %s ]"  %  (
                                    self.target_area.name, 
                                    datetime.strftime(
                                            self.last_update_time, 
                                            "%H:%M:%S %d-%m-%Y"
                                            ) 
                                    )  
        
 
    class Meta:
        ordering = ['-last_update_time', '-target_area__radius', 'target_area__name']

        unique_together = ('target_area', 'last_update_time')
        # altrimenti non ha senso salvare un altro record... se è lo stesso
        # metto il try nel momento del salvataggio

        verbose_name = "historical datapoint"  # Nome al singolare
        verbose_name_plural = "historical datapoints"  # Nome al plurale


# --------------------------------

# --------------------------------


class DatapointsSerieParameters(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'TargetArea',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    name = models.CharField(
        max_length=256, 
        blank=False, 
        null=False,
        help_text="""Declare a name for this set of parameters"""
        )

    description = models.TextField(null=False, blank=True)

    time_horizon = models.DurationField(
        null=False, 
        blank=False, 
        default=timedelta(days=1),
        help_text="""Set the time horizon (e.g., 1 day = 1 00:00:00)"""
        )
    
    aggregation_period = models.DurationField(
        null=False, 
        blank=False, 
        default=timedelta(hours=1),
        verbose_name="aggregation_period",
        help_text="""Set the aggregation period (e.g., 1 hour = 0 01:00:00)"""
        )

    show_serie = models.BooleanField( 
        null=False, 
        blank=False, 
        default=True ,
        verbose_name="show serie",
        help_text="Check this to show the series in the dashboard."
        ) 
    

    # dafult: create a time serie of 1h aggregation and having a 1-day time horizon

    def __str__(self):       
        return  "%s %s"  %  ( self.target_area.name , self.name )  
        
 
    class Meta:
        ordering = ['-target_area__radius', 'target_area__name']

        unique_together = ('time_horizon', 'aggregation_period')

        verbose_name = "datapoints serie parameters"  # Nome al singolare
        # verbose_name_plural = "datapoints_serie_parameters"  # Nome al plurale



class DatapointsSerieComputed(models.Model):

    # nota che è maiuscolo
    datapoints_serie_parameters = models.ForeignKey(
        'DatapointsSerieParameters',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    # postgres non prende array + datetime
    record_time_values = models.TextField( blank=False, null=False) 

    PM10_mean_values = models.TextField( null=False, blank=False)
    PM25_mean_values = models.TextField( null=False, blank=False)

    PM10_mean_cathegory_label_values = models.TextField( blank=False, null=False)
    PM25_mean_cathegory_label_values = models.TextField( blank=False, null=False)

    PM10_mean_cathegory_values  = models.TextField( blank=False, null=False)
    PM25_mean_cathegory_values = models.TextField( blank=False, null=False)

    number_of_contributing_sensors_values = models.TextField(null=True)

    PM10_graph_div = models.TextField()
    PM25_graph_div = models.TextField()



    def __str__(self):       
        return  "(DatapointsSerieComputed) %s %s"  %  ( self.datapoints_serie_parameters.name , self.datapoints_serie_parameters.name )  
        
 
    class Meta:
        ordering = [
            '-datapoints_serie_parameters__target_area__radius',
            'datapoints_serie_parameters__target_area__name'
            ]

        verbose_name = "datapoints serie computed"  # Nome al singolare
        # verbose_name_plural = "datapoints_series_computed"  # Nome al plurale
