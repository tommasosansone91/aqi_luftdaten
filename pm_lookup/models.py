from django.db import models
from django.utils import timezone
from datetime import datetime



# Create your models here.
# nota che i modelli sono tutti in minuscolo

# ogni modello django possiede per default
# id = models.AutoField(primary_key=True)

class target_area(models.Model):

    # id = models.AutoField(primary_key=True)

    # Ho reso il nome univoco così sono obbligato a specificare la diversità nel nome se anche cambio 
    # le coordinate del centro o il raggio
    Name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    Description = models.TextField(null=False, blank=False)

    Latitude = models.FloatField(null=False, blank=False)

    Longitude = models.FloatField(null=False, blank=False)

    Radius = models.FloatField(null=False, blank=False)
    # deve essere integer


    def __str__(self):       
        return  "%s --- [%s, %s - Radius: %s km]"  %    (
                                                        self.Name, 
                                                        self.Latitude, 
                                                        self.Longitude, 
                                                        self.Radius
                                                        )  

    class Meta:
        ordering = ['-Radius', 'Name']




class RealtimeDatapoints(models.Model):

    """
    Model to represent real-time air quality data for a specific target area.

    Fields:
        - target_area (OneToOneField): One-to-one association with the 'target_area' model.
        - Last_update_time (DateTimeField): Timestamp of the last data update (default: current time).
        - PM10_mean (FloatField): Average value of PM10 particles.
        - PM25_mean (FloatField): Average value of PM2.5 particles.
        - PM10_mean_quality_cathegory_label, PM25_mean_quality_cathegory_label (CharField): Descriptive air quality assessment (e.g., 'Good', 'Moderate').
        - PM10_category, PM25_category (CharField): Categorization based on average particle values.
        - number_of_contributing_sensors (IntegerField): Number of sensors used to compute the average data.

    Meta:
        - ordering: Default ordering by descending target area radius, then alphabetically by name.
    
    Methods:
        - __str__: Returns a readable string with the target area name and the timestamp of the last update.
    """

    # nota che è maiuscolo
    target_area = models.OneToOneField(
        'target_area',
        on_delete=models.CASCADE,
        
    )
    
    # name, radius lat e long le prendo dal target area input data (onetoonefield) usando il .Name. .Radius, ecc
    
    # Target_area_name = models.ForeignKey(
    #     'target_area',
    #     # Target_area_name = models.ForeignKey('target_area', on_delete....)
    #     # vuol dire: in questo campo metti l'id del modello 'target_area'
        
    #     # nota che l'attributo è in minuscolo
    #     on_delete=models.CASCADE,
    # )
    # il primo attributo è il modello cui è associato

    Last_update_time = models.DateTimeField(blank=False, null=False, default=timezone.now )

    # these could be switched to a single json

    PM10_mean = models.FloatField(null=False, blank=False)
    PM25_mean = models.FloatField(null=False, blank=False)

    PM10_mean_quality_cathegory_label = models.CharField(max_length=256, blank=False, null=False)
    PM25_mean_quality_cathegory_label = models.CharField(max_length=256, blank=False, null=False)

    PM10_mean_quality_cathegory = models.CharField(max_length=256, blank=False, null=False)
    PM25_mean_cathegory = models.CharField(max_length=256, blank=False, null=False)

    number_of_contributing_sensors = models.IntegerField(null=True)
    
    # PM10_n_missing_data = models.IntegerField(null=True)
    # PM25_n_missing_data = models.IntegerField(null=True)

    # PM10_n_missing_data = models.CharField(max_length=256, null=True)
    # PM25_n_missing_data = models.CharField(max_length=256, null=True)


    def __str__(self):       
        return  "%s --- [ %s ]"  %  (
                                    self.target_area.Name, 
                                    datetime.strftime(
                                        self.Last_update_time, 
                                        "%H:%M:%S %d-%m-%Y"
                                        ) 
                                    )  


    class Meta:
        ordering = ['-target_area__Radius', 'target_area__Name']
        # fixato così
        # ordering = ['-target_area.Radius', 'target_area.Name']

        verbose_name = "realtime_datapoint"  # Nome al singolare
        verbose_name_plural = "realtime_datapoints"  # Nome al plurale


class HistoricalDatapoints(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'target_area',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    Last_update_time = models.DateTimeField(blank=False, null=False, default=timezone.now )

    PM10_mean = models.FloatField(null=False, blank=False)
    PM25_mean = models.FloatField(null=False, blank=False)

    PM10_mean_quality_cathegory_label = models.CharField(max_length=256, blank=False, null=False)
    PM25_mean_quality_cathegory_label = models.CharField(max_length=256, blank=False, null=False)

    PM10_mean_quality_cathegory = models.CharField(max_length=256, blank=False, null=False)
    PM25_mean_cathegory = models.CharField(max_length=256, blank=False, null=False)

    number_of_contributing_sensors = models.IntegerField(null=True)

    # PM10_n_missing_data = models.IntegerField(null=True)
    # PM25_n_missing_data = models.IntegerField(null=True)

    # PM10_n_missing_data = models.CharField(max_length=256, null=True)
    # PM25_n_missing_data = models.CharField(max_length=256, null=True)


    def __str__(self):       
        return  "%s --- [ %s ]"  %  (
                                    self.target_area.Name, 
                                    datetime.strftime(
                                            self.Last_update_time, 
                                            "%H:%M:%S %d-%m-%Y"
                                            ) 
                                    )  
        
 
    class Meta:
        ordering = ['-Last_update_time', '-target_area__Radius', 'target_area__Name']

        # fixato così
        # ordering = ['-target_area.Radius', 'target_area.Name', '-Last_update_time']

        unique_together = ('target_area', 'Last_update_time', 'PM10_mean', 'PM25_mean')
        # altrimenti non ha senso salvare un altro record... se è lo stesso
        # metto il try nel momento del salvataggio

        verbose_name = "historical_datapoint"  # Nome al singolare
        verbose_name_plural = "historical_datapoints"  # Nome al plurale


# --------------------------------


class DatapointsSerie(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'target_area',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    # postgres non prende array + datetime
    Record_time_values = models.TextField( blank=False, null=False) 

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
        return  "%s"  %  (self.target_area.Name )  
        
 
    class Meta:
        ordering = ['-target_area__Radius', 'target_area__Name']

        verbose_name = "datapoints_serie"  # Nome al singolare
        verbose_name_plural = "datapoints_series"  # Nome al plurale



# serie orarie


class HourlyAggregatedDatapointsSerie(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'target_area',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    # postgres non prende array + datetime
    Record_time_values = models.TextField( blank=False, null=False) 

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
        return  "%s"  %  (self.target_area.Name )  
        
 
    class Meta:
        ordering = ['-target_area__Radius', 'target_area__Name']

        verbose_name = "hourly_aggregated_datapoints_serie"  # Nome al singolare
        verbose_name_plural = "hourly_aggregated_datapoints_series"  # Nome al plurale


# serie giornaliere

class DailyAggregatedDatapointsSerie(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'target_area',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    # postgres non prende array + datetime
    Record_time_values = models.TextField( blank=False, null=False) 

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
        return  "%s"  %  (self.target_area.Name )  
        
 
    class Meta:
        ordering = ['-target_area__Radius', 'target_area__Name']

        verbose_name = "daily_aggregated_datapoints_serie"  # Nome al singolare
        verbose_name_plural = "daily_aggregated_datapoints_series"  # Nome al plurale