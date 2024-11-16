from django.contrib import admin

from .models import target_area
from .models import realtime_datapoints
from .models import history_datapoints
from .models import datapoints_data_serie
from .models import daily_aggregated_data_serie

# Register your models here.
# admin.site.register(target_area)
# admin.site.register(realtime_datapoints)
# admin.site.register(history_datapoints)

# sono registrati in seguito mettendo in input anche il relativo modello Admin, 
# per permettere a sjango import export di funzionare


# per il tool import export
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# funzionano ma vs studio li legge male



# registrazione modello input

# questo modello controlla i field associati al tool import export, non all'admin
class target_areaResource(resources.ModelResource):

    class Meta:
        model = target_area
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class target_areaAdmin(ImportExportModelAdmin):
    resource_class = target_areaResource

admin.site.register(target_area, target_areaAdmin)


# registrazione modello realtime

# questo modello controlla i field associati al tool import export, non all'admin
class realtime_datapointsResource(resources.ModelResource):

    class Meta:
        model = realtime_datapoints
        
        # fields = ('id', 'name', 'price') # per includere i campi
        exclude = ('id') # per escludere i campi

class realtime_datapointsAdmin(ImportExportModelAdmin):
    resource_class = realtime_datapointsResource

admin.site.register(realtime_datapoints, realtime_datapointsAdmin)


#  registrazione modello history data

# questo modello controlla i field associati al tool import export, non all'admin
class history_datapointsResource(resources.ModelResource):

    class Meta:
        model = history_datapoints
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class history_datapointsAdmin(ImportExportModelAdmin):
    resource_class = history_datapointsResource

    # aggiungo il filtro laterale per selezionare a seconda della località
    list_filter = ['target_area__Name']

admin.site.register(history_datapoints, history_datapointsAdmin)


#  registrazione modello time series

# questo modello controlla i field associati al tool import export, non all'admin
class datapoints_data_serieResource(resources.ModelResource):

    class Meta:
        model = datapoints_data_serie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class datapoints_data_serieAdmin(ImportExportModelAdmin):
    resource_class = datapoints_data_serieResource

admin.site.register(datapoints_data_serie, datapoints_data_serieAdmin)



#  registrazione modello daily time series

# questo modello controlla i field associati al tool import export, non all'admin
class daily_aggregated_data_serieResource(resources.ModelResource):

    class Meta:
        model = daily_aggregated_data_serie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class daily_aggregated_data_serieAdmin(ImportExportModelAdmin):
    resource_class = daily_aggregated_data_serieResource

admin.site.register(daily_aggregated_data_serie, daily_aggregated_data_serieAdmin)