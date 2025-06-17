
# usage
#----------

# python manage.py test_extract_data_from_sensors_network_for_all_places

from django.core.management.base import BaseCommand

from pm_lookup.processing.utils.sensors_network_data_processing import extract_data_from_sensors_network_for_all_places

"""this is just for development/test"""


class Command(BaseCommand):
    def handle(self, *args, **options):

        sensors_network_data = extract_data_from_sensors_network_for_all_places()

        # print(sensors_network_data)