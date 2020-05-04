from django.contrib import admin

from .models import target_area_input_data
from .models import target_area_output_data
from .models import target_area_history_data

# Register your models here.
admin.site.register(target_area_input_data)
admin.site.register(target_area_output_data)
admin.site.register(target_area_history_data)