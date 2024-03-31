# in case there are problems with psycopg2

if

    pip install psycopg2

fails, try

    pip install psycopg2-binary

if it fails too, then run, in the virtualenv activated

    sudo apt-get install python-psycopg2

    sudo apt-get install libpq-dev