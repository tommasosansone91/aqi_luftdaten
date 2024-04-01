# this file must be given in input to gunicorn

import os
from django.core.wsgi import get_wsgi_application

# environment settings for Django app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqi_luftdaten.settings')

# Initialize app Django
application = get_wsgi_application()
