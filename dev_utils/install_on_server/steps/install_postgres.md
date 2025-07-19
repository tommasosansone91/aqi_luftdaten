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

diventa user postgres

    sudo -i -u postgres

apri la shell

    psql

reimposta la pw

    \password postgres

rootpassword
rootpassword

    exit

    psql -h localhost -U postgres -d postgres

    create database aqi_graphs_dashboard;

    create user aqigd_main WITH ENCRYPTED PASSWORD 'aqigdmain';  # choose short one
    create user aqigd_readonly WITH ENCRYPTED PASSWORD 'aqigdreadonly';  # choose short one

    alter database aqi_graphs_dashboard OWNER TO aqigd_main;

    exit

    psql -h localhost -U aqigd_main -d aqi_graphs_dashboard


--> questa configurazione risulta nelle seguenti credenziali

    'NAME': 'aqi_graphs_dashboard',
    'USER': 'aqigd_main',
    'PASSWORD': 'aqigdmain',

inserisci queste credenziali su settings.py (app di default creata da django)