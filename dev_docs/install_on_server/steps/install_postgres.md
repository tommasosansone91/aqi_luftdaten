# install postgresql

login sull EC2

### install


    sudo apt-get update
    sudo apt-get install postgresql


https://askubuntu.com/a/1466769/1342430

    sudo netstat -lntp | grep postgres
    sudo ufw allow 5432  # or other port


### configure


https://www.qunsul.com/posts/installing-postgresql-13-on-ubuntu-ec2-instance.html

    sudo -i -u postgres

    \password postgres

aqiluftdaten
aqiluftdaten

    exit

    psql -h localhost -U postgres -d postgres

    create database aqiluftdaten

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