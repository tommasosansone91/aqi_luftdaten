# Install on raspberry pi

This procedure is to install the app on a raspberry pi.

## key exchange between raspberry pi and github

    sudo su

    ssh-keygen -t ed25519 -C "tommaso.sansone91@virgilio.it"

    <kbd>enter</kbd>

    <insert password>

    <insert password>

questa diventa la pw da usare per sbloccare github sul tuo pc corrente

output:

    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/root/.ssh/id_ed25519): 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /root/.ssh/id_ed25519.
    Your public key has been saved in /root/.ssh/id_ed25519.pub.
    The key fingerprint is:

    ...

attiva l'agente ssh

    eval $(ssh-agent -s)

mi ritorna

>   Agent pid 716

aggiungi il file di chiave "agli ssh"

    ssh-add ~/.ssh/id_ed25519

inserisci la password

    cat ~/.ssh/id_ed25519.pub

e cio che è stampato la incollo nella pagina ad ssh key di github > settings > add ssh key

https://github.com/settings/ssh/new


## clone the app on raspberry pi

    sudo su

    cd /var/www/

usa il comando con l'url che inizia per https

    git clone https://github.com/tommasosansone91/aqi_luftdaten.git


## create virtual environment

    sudo su

    cd /var/www/aqi_luftdaten


### secondo il tutorial

crea un virtulaenv mettendo i suoi elementi 

- lib
- include
- bin
- pyvenv.cfg

nella cartella stessa, sanza raggrupparli

    /usr/local/opt/python-3.8.1/bin/python3.8 -m venv .

attivalo per test

    source ./bin/activate
    deactivate


### secondo me

crea un virtulaenv in una cartella venv

    /usr/local/opt/python-3.8.1/bin/python3.8 -m venv ./venv/

attivalo per test

    source venv/bin/activate
    deactivate


## install nginx

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate

    apt-get update
    apt-get install nginx

test it works by 

    hostname -I

    http://<IP>

you should see the nginx welcome page 


## install postgres

### install


    sudo apt-get update
    sudo apt-get install postgresql


https://askubuntu.com/a/1466769/1342430

    sudo netstat -lntp | grep postgres
    sudo ufw allow 5432  # or other port


### reset postgres default password


https://www.qunsul.com/posts/installing-postgresql-13-on-ubuntu-ec2-instance.html

diventa user postgres

    sudo -i -u postgres

apri la shell

    psql

reimposta la pw

    \password postgres

rootpassword
rootpassword

    exit

### create database for app

    psql -h localhost -U postgres -d postgres

    create database aqiluftdaten;

    create user luftdaten_main WITH ENCRYPTED PASSWORD 'aqimain';  # choose short one
    create user luftdaten_readonly WITH ENCRYPTED PASSWORD 'aqireadonly';  # choose short one

    alter database aqiluftdaten OWNER TO luftdaten_main;

    exit

    psql -h localhost -U luftdaten_main -d aqiluftdaten


--> questa configurazione risulta nelle seguenti credenziali

    'NAME': 'aqiluftdaten',
    'USER': 'luftdaten_main',
    'PASSWORD': 'aqimain',

inserisci queste credenziali su settings.py (app di default creata da django)


## install the web framework django

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate


prima bisogna installare postgresql, o ci saranno problemi con psycopg2

    sudo apt update

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
configura il db per essere connesso (settings.py).

setup the database via python 

    python manage.py makemigrations

    python manage.py migrate

    python manage.py createsuperuser

nei settings metti

    ALLOWED_HOSTS = ['*']

solo per test, poi blocca

    python manage.py runserver 0.0.0.0:8000

## web server - reverse proxy : nginx

### install

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate

    sudo apt-get install nginx

test:

    hostname -I

connettiti con il browser di un altro dispositivo sulla stessa lan al url

    http://<IP>

e dovresti vedere il welcome di nginx

### configuration

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate

the default file is at path

    /etc/nginx/sites-enabled/default
    /etc/nginx/sites-available/default

ma a noi non serve e lo cancelliamo

    rm /etc/nginx/sites-enabled/default

creo il file

> nginx/aqi_luftdaten_nginx.conf

eseguo link simbolico

    ln -s /var/www/aqi_luftdaten/nginx/aqi_luftdaten_nginx.conf /etc/nginx/conf.d/

dovresti vedere:

    root@Raspberry100:/etc/nginx/conf.d# ll
    total 8.0K
    lrwxrwxrwx 1 root root   35 Aug 24  2020 lab_app_nginx.conf -> /var/www/lab_app/lab_app_nginx.conf

stop the manually-started via manage.py server of the app.

restart nginx:

    /etc/init.d/nginx restart

test:

connect via browser to both

    http://<IP>:PORT_1  # port of another app
    http://<IP>:3000

the other app should still be reachable, while on port "http://<IP>:3000" you should get "502 bad gateway" as uWSGI is not configured yet.

in case of errors, to rollback:

    cd /etc/nginx/conf.d/
    rm /etc/nginx/conf.d/aqi_luftdaten_nginx.conf

    systemctl stop nginx.service
    systemctl start nginx.service
    systemctl status nginx.service

## web server for python: gunicorn

 è un server HTTP per Python WSGI (Web Server Gateway Interface). In altre parole, è un server web che è progettato per eseguire applicazioni web Python conformi allo standard WSGI.

### install

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate

    pip install gunicorn

### bind

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate

    PYTHONPATH=`pwd`/.. venv/bin/gunicorn aqi_luftdaten.wsgi:application --bind localhost:8000

https://stackoverflow.com/a/39461113/7658051

test:

you should see the app running at

http://192.168.1.106:3000/

from the browser of any other device connected to the network


### Start the app manually in background via gunicorn (and gracefully exit the machine)

> [!NOTE]
> This is just a temporary command and should be launched only to check that guincorn can run the app successfully.
> The starting, stopping and starting-at-boot of the app should be managed via systemd and the systemctl syntax, which should be implemented as last step of the app installation rpocess.

    current_dir=$pwd

Lancia manualmente copiando lo script e incollandolo nella shell comando per comando, o non funziona.

    cd /var/www/aqi_luftdaten/
    source venv/bin/activate

    sudo nohup env PYTHONPATH=`pwd`/.. venv/bin/gunicorn aqi_luftdaten.wsgi:application --bind localhost:8000 > /home/pi/aqi_luftdaten.log 2>&1 &


    cd $current_dir

#### check that the app is up and running

    echo "Grepping the app name from ps aux"
    echo "$(ps aux | grep 'aqi_luftdaten')"

#### exit the machine gracefully

    ctrl + D

> [!IMPORTANT]
> Do not use the X button of the UI of the terminal.


## cron files

the files in folder cron/ must be copied in directory

/etc/cron.d/

of the host server. 

No restart of cron is needed.

## log files

create directrory to host logs

    sudo mkdir /var/log/aqi_luftdaten/

## Turn the app into a service

deployed the files in folder systemd/ to

    /etc/systemd/system 

This will allow them to be ran on boot.

Once in the folder, make the file executable 

    sudo chmod +x aqi_luftdaten.service

Start the service 

    sudo systemctl start aqi_luftdaten.service

and check it is allright

    sudo systemctl status aqi_luftdaten.service

To make this service automatically run on boot

    sudo systemctl daemon-reload
    sudo systemctl enable aqi_luftdaten.service

Test that it works

> [!CAUTION]
> This will restart your machine.

    sudo reboot

In case you want to disable the program on boot

    sudo systemctl daemon-reload
    sudo systemctl disable aqi_luftdaten.service

Documentation https://www.freedesktop.org/software/systemd/man/systemd.service.html