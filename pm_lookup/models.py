from django.db import models


from datetime import datetime
from datetime import timedelta
from django.utils import timezone

import uuid

import asyncio
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async

from django.db.models.signals import post_save
from django.dispatch import receiver

from pm_lookup.configs.constants import COMPUTED_SERIE_META_VERBOSE_NAME, SET_OF_PARAMETERS_OF_SERIE_META_VERBOSE_NAME

from pm_lookup.processing.model_update_triggered_processing_1 import content_of_generate_series_and_draw_graphs



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

    async def generate_series_and_draw_graphs_async(self):
        await content_of_generate_series_and_draw_graphs()

    def generate_series_and_draw_graphs(self):
        # Create a thread pool executor
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the async function in the new event loop
        loop.run_in_executor(executor, self._run_async)

    def _run_async(self):
        asyncio.run(self.generate_series_and_draw_graphs_async())

    def save(self, *args, **kwargs):
        # First, save the instance
        super().save(*args, **kwargs) 
        print("Changes in model have been saved!") 
        print("Triggering the rebuilding and redrawing of the corresponding series!")
        
        # Then rebuild series and graphs
        self.generate_series_and_draw_graphs() 

        print("Serie rebuilding and redrawing has finished!")



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


# Using Django's post_save signal
@receiver(post_save, sender=SerieParametersSet)
def trigger_async_generation(sender, instance, **kwargs):
    instance.generate_series_and_draw_graphs()


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
