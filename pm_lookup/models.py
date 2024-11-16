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




class realtime_datapoints(models.Model):

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

    PM10_quality = models.CharField(max_length=256, blank=False, null=False)
    PM25_quality = models.CharField(max_length=256, blank=False, null=False)

    PM10_cathegory = models.CharField(max_length=256, blank=False, null=False)
    PM25_cathegory = models.CharField(max_length=256, blank=False, null=False)

    n_selected_sensors = models.IntegerField(null=True)
    
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



class history_data(models.Model):

    # nota che è maiuscolo
    target_area = models.ForeignKey(
        'target_area',
        on_delete=models.CASCADE,
        
    )
    # il primo attributo è il modello cui è associato

    Last_update_time = models.DateTimeField(blank=False, null=False, default=timezone.now )

    PM10_mean = models.FloatField(null=False, blank=False)
    PM25_mean = models.FloatField(null=False, blank=False)

    PM10_quality = models.CharField(max_length=256, blank=False, null=False)
    PM25_quality = models.CharField(max_length=256, blank=False, null=False)

    PM10_cathegory = models.CharField(max_length=256, blank=False, null=False)
    PM25_cathegory = models.CharField(max_length=256, blank=False, null=False)

    n_selected_sensors = models.IntegerField(null=True)

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

# --------------------------------


class datapoints_data_serie(models.Model):

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

    PM10_quality_values = models.TextField( blank=False, null=False)
    PM25_quality_values = models.TextField( blank=False, null=False)

    PM10_cathegory_values = models.TextField( blank=False, null=False)
    PM25_cathegory_values = models.TextField( blank=False, null=False)

    n_selected_sensors_values = models.TextField(null=True)

    PM10_graph_div = models.TextField()
    PM25_graph_div = models.TextField()



    def __str__(self):       
        return  "%s"  %  (self.target_area.Name )  
        
 
    class Meta:
        ordering = ['-target_area__Radius', 'target_area__Name']



# serie giornaliere

class daily_aggregated_data_serie(models.Model):

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

    PM10_quality_values = models.TextField( blank=False, null=False)
    PM25_quality_values = models.TextField( blank=False, null=False)

    PM10_cathegory_values = models.TextField( blank=False, null=False)
    PM25_cathegory_values = models.TextField( blank=False, null=False)

    n_selected_sensors_values = models.TextField(null=True)

    PM10_graph_div = models.TextField()
    PM25_graph_div = models.TextField()



    def __str__(self):       
        return  "%s"  %  (self.target_area.Name )  
        
 
    class Meta:
        ordering = ['-target_area__Radius', 'target_area__Name']