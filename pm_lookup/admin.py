from django.contrib import admin

from .models import target_area_input_data
from .models import target_area_output_data
from .models import target_area_history_data
# from .models import target_area_history_series

# Register your models here.
# admin.site.register(target_area_input_data)
# admin.site.register(target_area_output_data)
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
class target_area_output_dataResource(resources.ModelResource):

    class Meta:
        model = target_area_output_data
        
        # fields = ('id', 'name', 'price') # per includere i campi
        exclude = ('id') # per escludere i campi

class target_area_output_dataAdmin(ImportExportModelAdmin):
    resource_class = target_area_output_dataResource

admin.site.register(target_area_output_data, target_area_output_dataAdmin)


#  registrazione modello history data

# questo modello controlla i field associati al tool import export, non all'admin
class target_area_history_dataResource(resources.ModelResource):

    class Meta:
        model = target_area_history_data
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class target_area_history_dataAdmin(ImportExportModelAdmin):
    resource_class = target_area_history_dataResource

admin.site.register(target_area_history_data, target_area_history_dataAdmin)


# #  registrazione modello history series

# # questo modello controlla i field associati al tool import export, non all'admin
# class target_area_history_seriesResource(resources.ModelResource):

#     class Meta:
#         model = target_area_history_series
        
#         # fields = ('id', 'name', 'price') # per includere i campi
#         # exclude = ('id') # per escludere i campi

# class target_area_history_seriesAdmin(ImportExportModelAdmin):
#     resource_class = target_area_history_seriesResource

# admin.site.register(target_area_history_series, target_area_history_seriesAdmin)