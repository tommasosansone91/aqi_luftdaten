# install django app

    sudo apt update
    sudo apt install python3

    sudo apt-get install pip

    sudo apt install python3-virtualenv

    virtualenv venv

    source venv/bin/activate

    cat requirements.txt | xargs -n 1 pip install

togli 
== version 
da ogni libreria in requirements che dà problemi, e rilancia 

    cat requirements.txt | xargs -n 1 pip install


una volta installato postgres,
configura il db per essere connesso

in settings.py

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

setup the database via python 

    python manage.py makemigrations

    python manage.py migrate

    python manage.py createsuperuser

nei settings metti

    ALLOWED_HOSTS = ['*']

solo per test, poi blocca

    python manage.py runserver 0.0.0.0:8000
