from django.contrib import admin

from .models import TargetArea
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import DatapointsSerie
from .models import DailyAggregatedDatapointsSerie

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



# registrazione modello input

# questo modello controlla i field associati al tool import export, non all'admin
class TargetAreaResource(resources.ModelResource):

    class Meta:
        model = TargetArea
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class TargetAreaAdmin(ImportExportModelAdmin):
    resource_class = TargetAreaResource

admin.site.register(TargetArea, TargetAreaAdmin)


# registrazione modello realtime

# questo modello controlla i field associati al tool import export, non all'admin
class RealtimeDatapointsResource(resources.ModelResource):

    class Meta:
        model = RealtimeDatapoints
        
        # fields = ('id', 'name', 'price') # per includere i campi
        exclude = ('id') # per escludere i campi

class RealtimeDatapointsAdmin(ImportExportModelAdmin):
    resource_class = RealtimeDatapointsResource

admin.site.register(RealtimeDatapoints, RealtimeDatapointsAdmin)


#  registrazione modello history data

# questo modello controlla i field associati al tool import export, non all'admin
class HistoricalDatapointsResource(resources.ModelResource):

    class Meta:
        model = HistoricalDatapoints
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class HistoricalDatapointsAdmin(ImportExportModelAdmin):
    resource_class = HistoricalDatapointsResource

    # aggiungo il filtro laterale per selezionare a seconda della località
    list_filter = ['TargetArea__Name']

admin.site.register(HistoricalDatapoints, HistoricalDatapointsAdmin)


#  registrazione modello time series

# questo modello controlla i field associati al tool import export, non all'admin
class DatapointsSerieResource(resources.ModelResource):

    class Meta:
        model = DatapointsSerie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class DatapointsSerieAdmin(ImportExportModelAdmin):
    resource_class = DatapointsSerieResource

admin.site.register(DatapointsSerie, DatapointsSerieAdmin)



#  registrazione modello daily time series

# questo modello controlla i field associati al tool import export, non all'admin
class DailyAggregatedDatapointsSerieResource(resources.ModelResource):

    class Meta:
        model = DailyAggregatedDatapointsSerie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class DailyAggregatedDatapointsSerieAdmin(ImportExportModelAdmin):
    resource_class = DailyAggregatedDatapointsSerieResource

admin.site.register(DailyAggregatedDatapointsSerie, DailyAggregatedDatapointsSerieAdmin)