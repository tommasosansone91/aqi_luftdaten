from django.db import models
from django.utils import timezone

# Create your models here.
# nota che i modelli sono tutti in minuscolo

class target_area_input_data(models.Model):

    Name = models.CharField(max_length=256, blank=False, null=False, unique=True)

    Latitude = models.FloatField(null=False, blank=False)

    Longitude = models.FloatField(null=True, blank=True)

    Radius = models.FloatField(null=False, blank=False)
    # deve essere integer


    def __str__(self):    
    # print("%s is %d years old." % (name, age))    
        return  "%s"  %  (self.Name)  
        #quello che fa apparire nella sezione admin, attributo che riassume tutti gli altri, quindi una primary key presumibilmente, pouò anche esesere la combinazione degli altri


class target_area_output_data(models.Model):

    # nota che è maiuscolo
    Target_area_name = models.ForeignKey(
        'target_area_input_data',

        # nota che l'attributo è in minuscolo
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
    # n_selected_sensors = models.CharField(max_length=256, null=True)

    PM10_n_missing_data = models.IntegerField(null=True)
    PM25_n_missing_data = models.IntegerField(null=True)

    # PM10_n_missing_data = models.CharField(max_length=256, null=True)
    # PM25_n_missing_data = models.CharField(max_length=256, null=True)


    def __str__(self):       
        return  "%s - %s"  %  (self.Target_area_name, self.Last_update_time)  

# --------------------------------

    #     def __str__(self):    
    #     # print("%s is %d years old." % (name, age))    
    #     return  "%s - %s ----- [%s] - [%s] - [%s]"  %  (self.Lemma_it, self.Lemma_ch, self.Id_statico_entry, self.Data_inserimento_entry, self.Admin_approval_switch)  
    #     #quello che fa apparire nella sezione admin, attributo che riassume tutti gli altri, quindi una primary key presumibilmente, pouò anche esesere la combinazione degli altri


    # class Meta:
    #     ordering = ['Admin_approval_switch', 'Lemma_it', 'Lemma_ch', 'Data_inserimento_entry', 'Id_statico_entry']
    #     # il meno davanti all'attributo vuol dire che ordina al contrario
    #     # '-Admin_approval_switch', 
    #     # faccio comparire per primi gli hide-> nuovi inseriti
    #     # in realtà per come ho definito hide e show, se metto senza il meno davanti, mi mostra per prima hide (h viene prima di s)

    # def clean(self):
    #  # necessario solo se non c'è il vincolo not null
    #     if not (self.Lemma_it or self.Acronimo_it or self.Definizione_it or self.Lemma_ch or self.Acronimo_ch or self.Definizione_ch):
    #         raise ValidationError("Non è stata inserita alcuna terminologia. Compilare almeno un campo del form.")
    #     # non mi restituisce questa scritta ma quella messa di default nelle views
