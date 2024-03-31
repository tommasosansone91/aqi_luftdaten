# deploy app on aws EC2 ubuntu

## crea macchina su aws


aws console

new ec2 instance

scegli os ubuntu

create key .pem

chiamala col nome dell'app che vai a caricarci, solo per chiarezza

es 
aqi_luftdaten.pem

allow http traffic flag sì

lancia

salvat l'ip publbico (a ogni stop di ec2 instance cambia)


## entra nella vm

vai nella cartella di linux dove hai salvato la .pem

    chmod 400 aqi_luftdaten.pem

    ssh -i aqi_luftdaten.pem ec2-user@<ip_publbico_istanza>

->entra nella vm


-----------------------------------------


## creazione db


vedi altro file

> dev_docs/install_on_server/install_postgres_on_any_server.txt


## installa git


    sudo apt update
    sudo apt install git

se serve, scambia chiavi git
vedi file

> dev_docs/install_on_server/steps/scambio_chiavi_github.txt


## deploy app

    git clone https://github.com/tommasosansone91/aqi_luftdaten.git

    cd aqi_luftdaten/


## installa app

vedi altro file

> dev_docs/install_on_server/steps/install_app.txt

(ho rimosso tutti i riferimenti a heroku e messo una secret key visibile)



## lancia app

    python manage.py runserver 0.0.0.0:8000


## apertura porta 8000 della EC2


su aws consolle

instanza > security tab > security grup id link > edit inbound security rules 

lasica la parte del ssh

aggiungi 
type: custom tcp
porta: 8000
source: custom
ip: 0.0.0.0


Name
Security group rule ID
IP version
Type
Protocol
Port range
Source
Description

–
sgr-076cb5b6fc4f4c351	
IPv4	
Custom TCP	
TCP	
8000	
0.0.0.0/0	
http port 8000


## accesso da browser


vai a http://15.161.126.254:8000/

dovrebbe funzionare

loggati con l'admin e crea i dati x far funzionare il db

