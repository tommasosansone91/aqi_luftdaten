"""
Django settings for aqi_luftdaten project.

Generated by 'django-admin startproject' using Django 2.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os 
# import django_heroku ###
# from decouple import config ###

# per gestire user e password del database postgresql che cambiano ogni 24 ore sugli host
# import dj_database_url ###

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config("SECRET_KEY")
SECRET_KEY = '45y9gh347qog4f9q8jfe08wg98np3u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'import_export',
    'pm_lookup',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware', #zips up static files
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aqi_luftdaten.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aqi_luftdaten.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# most simple config with sqlite3

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aqiluftdaten',
        'USER': 'luftdaten_main',
        'PASSWORD': 'aqimain',
        'HOST': 'localhost',
        # 'HOST': '0.0.0.0',
        'PORT': '5432',
    }
}


# old heroku-postgres config
# ----------------------------

# database__default_credential_url= config("DATABASE_URL")

# DATABASES['default']=dj_database_url.config(default=database__default_credential_url)

# # #postgres://user:password@host:porta/database_name

# # questi sono settings minori
# db_from_env=dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

# -------------------------------

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Queste tre linee e aggiungo io
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICSTORAGE = "Whitenoise.storage.CompressedManifestStaticFilesStorage" #zips up static files

# django_heroku.settings(locals())  ###

#aggiunto per far funzionare il modulo di importazione csv in admin
IMPORT_EXPORT_USE_TRANSACTIONS = True

# aggiunto per aumentare a 10000 il numero massimo di campi che posso cancellare dai modelli tramite l'admin di django
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000


