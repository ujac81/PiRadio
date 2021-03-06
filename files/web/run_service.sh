#!/bin/bash

if [ "x$DEBUG" = "x1" ]; then

    echo "Starting in DEBUG mode...."
    cd /code
    python3 manage.py migrate
    python3 manage.py collectstatic --no-input
    python3 manage.py runserver 0.0.0.0:8000


elif [ "x$COLLECT" = "x1" ]; then

    echo "Starting in COLLECT mode...."
    cd /code
    python3 manage.py migrate
    python3 manage.py compress --extension=pug --force
    python3 manage.py collectstatic --no-input
    rsync -rptgo --delete --size-only /code/static/* /static
    uwsgi --ini /etc/uwsgi/uwsgi.ini
    
else

    cd /code
    echo "Starting in release mode...."
    python3 manage.py migrate
    rsync -rptgo --delete --size-only /code/static/* /static
    uwsgi --ini /etc/uwsgi/uwsgi.ini
fi
