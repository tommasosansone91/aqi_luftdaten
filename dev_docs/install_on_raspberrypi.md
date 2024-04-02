# Install on Raspberry pi

This procedure is to install the app aqi_luftdaten on a Raspberry pi.

> [!IMPORTANT]
> The Raspberry pi and the PC must be connected to the same LAN network.

## Key exchange between RPi and github

from your PC log into the RPi.

    ssh pi@<RPi_IP>

    <password>

become admin

    sudo su

    ssh-keygen -t ed25519 -C "your_mail_address@your_dominion.it"

press <kbd>enter</kbd>

    <password>

    <password>

> [!IMPORTANT]
> This password becomes the password you have to give in from the RPi to interact with github (e.g. `git clone`), so note it down..

output:

    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/root/.ssh/id_ed25519): 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /root/.ssh/id_ed25519.
    Your public key has been saved in /root/.ssh/id_ed25519.pub.
    The key fingerprint is:

    ...

activate the ssh agent

    eval $(ssh-agent -s)

this should return

>    Agent pid 716

add the new .ssh file to the files recognized by the ssh agent

    ssh-add ~/.ssh/id_ed25519

    <password>

get the content of the file ending with `.pub`

    cat ~/.ssh/id_ed25519.pub

copy the output of this command (it should start with `ssh-ed25519 ` and end with the e-mail address)

log in into your github account and go to

https://github.com/settings/ssh/new

> github profile > top-right dropdown menu > settings > left-side menu > SSH and GPG keys > add ssh key

> [!TIP]
> Choose a self-explanatory title, such as 
> `id_ed25519.pub_from_RPi_model4B_4GB`
> so that you will remember which device it is associated to.


## Clone the app on raspberry pi

from your PC log into the RPi.

    ssh pi@<RPi_IP>

    <password>

become admin

    sudo su

Go to the directory where we want to install the app

    cd /var/www/

get the git clone link from github:

- go to the github repo
- `Code` button
- `HTTPS` tab
- copy the link

> [!NOTE]
> Do not use the github link starting with git@...

    git clone https://github.com/tommasosansone91/aqi_luftdaten.git


## Install Nginx as web server and reverse proxy

This is the *web server* (server the static files) and *reverse proxy* (forwards the dynamic requests to Django).

    sudo su
    cd /var/www/aqi_luftdaten
    source venv/bin/activate

    apt-get update
    apt-get install nginx

test that it works by running

    hostname -I

then place in your browser the URL

    http://<RPi_IP>

you should see the nginx welcome page.


## Install Postgresql database

### Install

    sudo apt-get update
    sudo apt-get install postgresql

Check the port on which postgres is listening

    sudo netstat -lntp | grep postgres

### Reset root default password

Useful information for Ubuntu: https://askubuntu.com/a/1466769/1342430

Useful information for AWS EC2: https://www.qunsul.com/posts/installing-postgresql-13-on-ubuntu-ec2-instance.html

The default password for postgresql is `postgres`, but it is better to change it for security reasons.

Become user `postgres`

    sudo -i -u postgres

open the postgres shell

    psql

reset the root password

    \password postgres

> [!CAUTION]
> This will become the new root password of postgres.
> If you forget this, you will not be able to manage postgresql anymore, so **note it down**.

    rootpassword

    rootpassword

commit the change by exiting the shell

    exit

### Create a new database for the app

enter the postgres shell as `postgres` user

    psql -h localhost -U postgres -d postgres

create the new database

    create database aqiluftdaten;

create a "main" and a "readonly" user for the app

    create user luftdaten_main WITH ENCRYPTED PASSWORD 'aqimain';  # choose short one

    create user luftdaten_readonly WITH ENCRYPTED PASSWORD 'aqireadonly';  # choose short one

make the main user the owner of the database

    alter database aqiluftdaten OWNER TO luftdaten_main;

exit the shell and test to reopen it as the "main user of the app"

    exit

    psql -h localhost -U luftdaten_main -d aqiluftdaten


> [!IMPORTANT]
> The database name, the database-owner user and its password become the credentials for the Django app to access the database.

    'NAME': 'aqiluftdaten',
    'USER': 'luftdaten_main',
    'PASSWORD': 'aqimain',

These credentials must be inserted in the `DATABASES` variable in `settings.py` module of the Django main app (the one created by default by django, at the same folder level of the other django apps inside that Django project).


## Install Python

    sudo add-apt-repository ppa:deadsnakes/ppa

    sudo apt update

    sudo apt install python3.8

## Install pip and virtulaenv

    sudo apt-get install pip

    sudo apt install python3-virtualenv


## create virtual environment

    sudo su

    cd /var/www/aqi_luftdaten

create virtual environment in folder `venv`

    /usr/local/opt/python-3.8.1/bin/python3.8 -m venv ./venv/

or whatever verion of python you have

attivalo e disaper test

    source venv/bin/activate
    deactivate

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