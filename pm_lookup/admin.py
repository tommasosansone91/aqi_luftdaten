from django import forms
from django.contrib import admin

from .models import AreaParametersSet
from .models import RealtimeDatapoint
from .models import HistoricalDatapoint
from .models import SerieParametersSet
from .models import ComputedSerie

# Register your models here.
# admin.site.register(AreaParametersSet)
# admin.site.register(RealtimeDatapoint)
# admin.site.register(HistoricalDatapoint)

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


class AreaParametersSetAdminForm(forms.ModelForm):
    
    class Meta:
        model = AreaParametersSet
        fields = '__all__'  # Include all fields in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if the object already exists
            self.fields['latitude'].widget.attrs['readonly'] = True
            self.fields['longitude'].widget.attrs['readonly'] = True
            self.fields['radius'].widget.attrs['readonly'] = True


class AreaParametersSetAdmin(ImportExportModelAdmin):
    resource_class = AreaParametersSetResource
    
    form = AreaParametersSetAdminForm

admin.site.register(AreaParametersSet, AreaParametersSetAdmin)


# registrazione modello RealtimeDatapoint
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class RealtimeDatapointResource(resources.ModelResource):

    class Meta:
        model = RealtimeDatapoint
        
        # fields = ('id', 'name', 'price') # per includere i campi
        exclude = ('id') # per escludere i campi

class RealtimeDatapointAdmin(ImportExportModelAdmin):
    resource_class = RealtimeDatapointResource

    # Adding the 'uuid' field to the readonly fields list - it is not editable, yet visible
    readonly_fields = ('uuid',)
    # @note: this line is not related to ImportExportModel plugin

admin.site.register(RealtimeDatapoint, RealtimeDatapointAdmin)


#  registrazione modello HistoricalDatapoint
#--------------------------------------------------

# questo modello controlla i field associati al tool import export, non all'admin
class HistoricalDatapointResource(resources.ModelResource):

    class Meta:
        model = HistoricalDatapoint
        
        # fields = ('id', 'name', 'price') # per includere i campi
        # exclude = ('id') # per escludere i campi

class HistoricalDatapointAdmin(ImportExportModelAdmin):
    # note:
    # ImportExportModel is just the class (one of the classes) HistoricalDatapointAdmin inherits from
    resource_class = HistoricalDatapointResource

    # Adding the 'uuid' field to the readonly fields list - it is not editable, yet visible
    readonly_fields = ('uuid',)
    # @note: this line is not related to ImportExportModel plugin

    # aggiungo il filtro laterale per selezionare a seconda della area di interesse
    list_filter = ['area_parameters_set__name']

admin.site.register(HistoricalDatapoint, HistoricalDatapointAdmin)


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

