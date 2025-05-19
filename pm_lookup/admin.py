from django.contrib import admin

from .models import AreaParametersSet
from .models import RealtimeDatapoints
from .models import HistoricalDatapoints
from .models import SerieParametersSet
from .models import ComputedSerie

# Register your models here.
# admin.site.register(AreaParametersSet)
# admin.site.register(RealtimeDatapoints)
# admin.site.register(HistoricalDatapoints)

# sono registrati in seguito mettendo in input anche il relativo modello Admin, 
# per permettere a sjango import export di funzionare


# per il tool import export
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# funzionano ma vs studio li legge male



# registrazione modello AreaParametersSet
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class AreaParametersSetResource(resources.ModelResource):

    class Meta:
        model = AreaParametersSet
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class AreaParametersSetAdmin(ImportExportModelAdmin):
    resource_class = AreaParametersSetResource

admin.site.register(AreaParametersSet, AreaParametersSetAdmin)


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
    list_filter = ['area_parameters_set__name']

admin.site.register(HistoricalDatapoints, HistoricalDatapointsAdmin)


#  registrazione modello SerieParametersSet
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class SerieParametersSetResource(resources.ModelResource):

    class Meta:
        model = SerieParametersSet
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class SerieParametersSetAdmin(ImportExportModelAdmin):
    resource_class = SerieParametersSetResource

admin.site.register(SerieParametersSet, SerieParametersSetAdmin)


#  registrazione modello ComputedSerie
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class ComputedSerieResource(resources.ModelResource):

    class Meta:
        model = ComputedSerie
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class ComputedSerieAdmin(ImportExportModelAdmin):
    resource_class = ComputedSerieResource

admin.site.register(ComputedSerie, ComputedSerieAdmin)

