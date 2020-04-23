from django.contrib import admin

from .models import target_area_input_data, target_area_output_data

# Register your models here.
admin.site.register(target_area_input_data)
admin.site.register(target_area_output_data)