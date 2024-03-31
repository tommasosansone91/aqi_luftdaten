# in case there are problems with psycopg2

if

    pip install psycopg2

fails, try

    pip install psycopg2-binary

if it fails too,

> You need to install postgresql-server-dev-X.Y for building a server-side extension or libpq-dev for building a client-side application

https://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi

then run, in the virtualenv activated

    sudo apt-get install python-psycopg2

    sudo apt-get install libpq-dev