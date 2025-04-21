from django.contrib import admin

from .models import TargetArea
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import DatapointsSerieParameters
from .models import DatapointsSerieComputed

# Register your models here.
# admin.site.register(TargetArea)
# admin.site.register(RealtimeDatapoints)
# admin.site.register(HistoricalDatapoints)

# sono registrati in seguito mettendo in input anche il relativo modello Admin, 
# per permettere a sjango import export di funzionare


# per il tool import export
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# funzionano ma vs studio li legge male



# registrazione modello TargetArea
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class TargetAreaResource(resources.ModelResource):

    class Meta:
        model = TargetArea
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class TargetAreaAdmin(ImportExportModelAdmin):
    resource_class = TargetAreaResource

admin.site.register(TargetArea, TargetAreaAdmin)


# registrazione modello RealtimeDatapoints
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class RealtimeDatapointsResource(resources.ModelResource):

    class Meta:
        model = RealtimeDatapoints
        
        # fields = ('id', 'name', 'price') # per includere i campi
        exclude = ('id') # per escludere i campi

class RealtimeDatapointsAdmin(ImportExportModelAdmin):
    resource_class = RealtimeDatapointsResource

admin.site.register(RealtimeDatapoints, RealtimeDatapointsAdmin)


#  registrazione modello HistoricalDatapoints
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class HistoricalDatapointsResource(resources.ModelResource):

    class Meta:
        model = HistoricalDatapoints
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class HistoricalDatapointsAdmin(ImportExportModelAdmin):
    resource_class = HistoricalDatapointsResource

    # aggiungo il filtro laterale per selezionare a seconda della area di interesse
    list_filter = ['target_area__name']

admin.site.register(HistoricalDatapoints, HistoricalDatapointsAdmin)


#  registrazione modello DatapointsSerieParameters
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class DatapointsSerieParametersResource(resources.ModelResource):

    class Meta:
        model = DatapointsSerieParameters
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class DatapointsSerieParametersAdmin(ImportExportModelAdmin):
    resource_class = DatapointsSerieParametersResource

admin.site.register(DatapointsSerieParameters, DatapointsSerieParametersAdmin)


#  registrazione modello DatapointsSerieComputed
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class DatapointsSerieComputedResource(resources.ModelResource):

    class Meta:
        model = DatapointsSerieComputed
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class DatapointsSerieComputedAdmin(ImportExportModelAdmin):
    resource_class = DatapointsSerieComputedResource

admin.site.register(DatapointsSerieComputed, DatapointsSerieComputedAdmin)

