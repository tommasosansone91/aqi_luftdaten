from django.contrib import admin

from .models import target_area_input_data
from .models import target_area_realtime_data
from .models import target_area_history_data
from .models import target_area_time_serie
from .models import target_area_daily_time_serie

# Register your models here.
# admin.site.register(target_area_input_data)
# admin.site.register(target_area_realtime_data)
# admin.site.register(target_area_history_data)

# sono registrati in seguito mettendo in input anche il relativo modello Admin, 
# per permettere a sjango import export di funzionare


# per il tool import export
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# funzionano ma vs studio li legge male



# registrazione modello input

# questo modello controlla i field associati al tool import export, non all'admin
class target_area_input_dataResource(resources.ModelResource):

    class Meta:
        model = target_area_input_data
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class target_area_input_dataAdmin(ImportExportModelAdmin):
    resource_class = target_area_input_dataResource

admin.site.register(target_area_input_data, target_area_input_dataAdmin)


# registrazione modello realtime

# questo modello controlla i field associati al tool import export, non all'admin
class target_area_realtime_dataResource(resources.ModelResource):

    class Meta:
        model = target_area_realtime_data
        
        # fields = ('id', 'name', 'price') # per includere i campi
        exclude = ('id') # per escludere i campi

class target_area_realtime_dataAdmin(ImportExportModelAdmin):
    resource_class = target_area_realtime_dataResource

admin.site.register(target_area_realtime_data, target_area_realtime_dataAdmin)


#  registrazione modello history data

# questo modello controlla i field associati al tool import export, non all'admin
class target_area_history_dataResource(resources.ModelResource):

    class Meta:
        model = target_area_history_data
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class target_area_history_dataAdmin(ImportExportModelAdmin):
    resource_class = target_area_history_dataResource

    # aggiungo il filtro laterale per selezionare a seconda della località
    list_filter = ['Target_area_input_data__Name']

admin.site.register(target_area_history_data, target_area_history_dataAdmin)


#  registrazione modello time series

# questo modello controlla i field associati al tool import export, non all'admin
class target_area_time_serieResource(resources.ModelResource):

    class Meta:
        model = target_area_time_serie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class target_area_time_serieAdmin(ImportExportModelAdmin):
    resource_class = target_area_time_serieResource

admin.site.register(target_area_time_serie, target_area_time_serieAdmin)



#  registrazione modello daily time series

# questo modello controlla i field associati al tool import export, non all'admin
class target_area_daily_time_serieResource(resources.ModelResource):

    class Meta:
        model = target_area_daily_time_serie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class target_area_daily_time_serieAdmin(ImportExportModelAdmin):
    resource_class = target_area_daily_time_serieResource

admin.site.register(target_area_daily_time_serie, target_area_daily_time_serieAdmin)