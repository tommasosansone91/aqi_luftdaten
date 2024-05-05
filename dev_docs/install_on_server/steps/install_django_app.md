# install django app

prima bisogna installare postgresql, o ci saranno problemi con psycopg2

    sudo apt update

    sudo apt install python3

    sudo apt-get install pip

    sudo apt install python3-virtualenv

    virtualenv venv
    source venv/bin/activate

per evitare problemi con l'installazione di psycopg2

    sudo apt-get install python-psycopg2

    sudo apt-get install libpq-dev

infine installazione massiva dei prerequisiti

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

    python manage.py runserver 0.0.0.0:8001
