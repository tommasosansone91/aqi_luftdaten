
# usage
# --------

# python manage.py generate_series_and_draw_graphs

from django.core.management.base import BaseCommand

from pm_lookup.configs.constants import ASYNCHRONOUS_COMPONENTS_TOOLBOX_CALLER_CHOICE_BASECOMMAND

from pm_lookup.processing.asynchronous_components_1 import AsynchronousComponentsToolbox1

"""
This command is to recreate the time series 
getting data from the  history data model.
It also recreates the graphs.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):

        #arrangia le serie storiche attingendo al modello storico grezzo e ridisegna i grafici

        print("BaseCommand generate_series_and_draw_graphs - S")

        caller = ASYNCHRONOUS_COMPONENTS_TOOLBOX_CALLER_CHOICE_BASECOMMAND
        model_update_processing_1 = AsynchronousComponentsToolbox1(caller)

        print("Generated instance model_update_processing_2 of class AsynchronousComponentsToolbox2!")

        print("Triggering the rebuilding and redrawing of the corresponding series!")
        model_update_processing_1.generate_series_and_draw_graphs() 

        print("Triggered the rebuilding and redrawing of the corresponding series!")
        print("Wait for the serie rebuilding and redrawing to finish...") 

        print("BaseCommand generate_series_and_draw_graphs - E")
