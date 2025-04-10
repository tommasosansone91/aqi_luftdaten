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

    """
    Represents a geographical area with a defined center and radius.

    Fields:
        - name (CharField): A unique name for the target area, used to identify it. 
          Must be unique to differentiate areas even if coordinates or radius change.
        - description (TextField): An optional description of the target area. Blank is allowed but not null.
        - latitude (FloatField): The latitude coordinate of the center of the target area.
        - longitude (FloatField): The longitude coordinate of the center of the target area.
        - radius (FloatField): The radius of the target area in kilometers. This defines the size of the area.

    Meta:
        - ordering: Target areas are ordered by descending radius size and then by name.
        - unique_together: Ensures that the combination of latitude, longitude, and radius is unique, 
          preventing duplicate entries for areas with identical geometry.

    Methods:
        - __str__: Returns a readable string representation of the target area, 
          including the name, coordinates, and radius.

    Example:
        A target area with name "Central Park", latitude 40.785091, longitude -73.968285, and radius 2.5 km:
            "Central Park --- [40.785091, -73.968285 - radius: 2.5 km]
    """

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
        return  "%s --- [%s, %s - radius: %s km]"  %    (
                                                        self.name, 
                                                        self.latitude, 
                                                        self.longitude, 
                                                        self.radius
                                                        )  

    class Meta:
        ordering = ['-radius', 'name']

        unique_together = ('latitude', 'longitude', 'radius')




class RealtimeDatapoints(models.Model):

    """
    Model to represent real-time air quality data for a specific target area.

    Fields:
        - TargetArea (OneToOneField): One-to-one association with the 'TargetArea' model.
        - last_update_time (DateTimeField): Timestamp of the last data update (default: current time).
        - PM10_mean (FloatField): Average value of PM10 particles.
        - PM25_mean (FloatField): Average value of PM2.5 particles.
        - PM10_mean_quality_cathegory_label, PM25_mean_quality_cathegory_label (CharField): Descriptive air quality assessment (e.g., 'Good', 'Moderate').
        - PM10_category, PM25_category (CharField): Categorization based on average particle values.
        - number_of_contributing_sensors (PositiveIntegerField): Number of sensors used to compute the average data.

    Meta:
        - ordering: Default ordering by descending target area radius, then alphabetically by name.
    
    Methods:
        - __str__: Returns a readable string with the target area name and the timestamp of the last update.
    """

    # nota che è maiuscolo
    TargetArea = models.OneToOneField(
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

    def __str__(self):       
        return  "%s --- [ %s ]"  %  (
                                    self.TargetArea.name, 
                                    datetime.strftime(
                                        self.last_update_time, 
                                        "%H:%M:%S %d-%m-%Y"
                                        ) 
                                    )  


    class Meta:
        ordering = ['-TargetArea__radius', 'TargetArea__name']
        # fixato così
        # ordering = ['-TargetArea.radius', 'TargetArea.name']

        verbose_name = "realtime_datapoint"  # Nome al singolare
        verbose_name_plural = "realtime_datapoints"  # Nome al plurale


class HistoricalDatapoints(models.Model):
    
    """
    Represents historical air quality data for a specific target area.

    Fields:
        - TargetArea (ForeignKey): A many-to-one relationship with the 'TargetArea' model.
        - last_update_time (DateTimeField): The timestamp indicating when the data was last updated.
        - PM10_mean (FloatField): The average concentration of PM10 particles.
        - PM25_mean (FloatField): The average concentration of PM2.5 particles.
        - PM10_mean_quality_cathegory_label (CharField): A descriptive label for the PM10 quality category (e.g., 'Good', 'Moderate').
        - PM25_mean_quality_cathegory_label (CharField): A descriptive label for the PM2.5 quality category.
        - PM10_mean_quality_cathegory (CharField): The quality category for PM10 as a code or identifier.
        - PM25_mean_cathegory (CharField): The quality category for PM2.5 as a code or identifier.
        - number_of_contributing_sensors (PositiveIntegerField): The number of sensors contributing to the average calculation.

    Meta:
        - ordering: Data is ordered by descending update time, then by descending target area radius, and finally by the target area name.
        - unique_together: Ensures that a combination of 'TargetArea' and 'last_update_time' is unique, preventing duplicate records for the same area and timestamp.
        - verbose_name: Singular name displayed in the Django Admin ("historical_datapoint").
        - verbose_name_plural: Plural name displayed in the Django Admin ("historical_datapoints").

    Methods:
        - __str__: Returns a readable string representation of the data point, including the target area's name and the last update timestamp.
    """

    # nota che è maiuscolo
    TargetArea = models.ForeignKey(
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
                                    self.TargetArea.name, 
                                    datetime.strftime(
                                            self.last_update_time, 
                                            "%H:%M:%S %d-%m-%Y"
                                            ) 
                                    )  
        
 
    class Meta:
        ordering = ['-last_update_time', '-TargetArea__radius', 'TargetArea__name']

        # fixato così
        # ordering = ['-TargetArea.radius', 'TargetArea.name', '-last_update_time']

        unique_together = ('TargetArea', 'last_update_time')
        # altrimenti non ha senso salvare un altro record... se è lo stesso
        # metto il try nel momento del salvataggio

        verbose_name = "historical_datapoint"  # Nome al singolare
        verbose_name_plural = "historical_datapoints"  # Nome al plurale


# --------------------------------

# --------------------------------


class DatapointsSerieParameters(models.Model):

    # nota che è maiuscolo
    TargetArea = models.ForeignKey(
        'TargetArea',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    name = models.CharField(max_length=256, blank=False, null=False)

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
        return  "%s %s"  %  ( self.TargetArea.name )  
        
 
    class Meta:
        ordering = ['-TargetArea__radius', 'TargetArea__name']

        unique_together = ('time_horizon', 'aggregation_period')

        verbose_name = "datapoints_serie"  # Nome al singolare
        verbose_name_plural = "datapoints_series"  # Nome al plurale



class DatapointsSerieComputed(models.Model):

    # nota che è maiuscolo
    Datapoints_serie_parameters = models.ForeignKey(
        'DatapointsSerieParameters',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    # postgres non prende array + datetime
    record_time_values = models.TextField( blank=False, null=False) 

    PM10_mean_values = models.TextField( null=False, blank=False)
    PM25_mean_values = models.TextField( null=False, blank=False)

    PM10_mean_quality_cathegory_label_values = models.TextField( blank=False, null=False)
    PM25_mean_quality_cathegory_label_values = models.TextField( blank=False, null=False)

    PM10_mean_quality_cathegory_values = models.TextField( blank=False, null=False)
    PM25_mean_cathegory_values = models.TextField( blank=False, null=False)

    number_of_contributing_sensors_values = models.TextField(null=True)

    PM10_graph_div = models.TextField()
    PM25_graph_div = models.TextField()



    def __str__(self):       
        return  "%s"  %  ( self.TargetArea.name )  
        
 
    class Meta:
        ordering = [
            '-Datapoints_serie_parameters__TargetArea__radius',
            'Datapoints_serie_parameters__TargetArea__name'
            ]

        verbose_name = "datapoints_serie"  # Nome al singolare
        verbose_name_plural = "datapoints_series"  # Nome al plurale
