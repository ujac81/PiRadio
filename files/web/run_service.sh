#!/bin/bash




if [ "x$DEBUG" = "x1" ]; then

    echo "Starting in DEBUG mode...."
    uwsgi --ini /etc/uwsgi/uwsgi.ini --python-autoreload 1
    
else

    cd /code
    echo "Starting in release mode...."
    python3 manage.py migrate && \
    python3 manage.py compress --extension=pug --force && \
    python3 manage.py collectstatic --no-input &&  \
    uwsgi --ini /etc/uwsgi/uwsgi.ini
fi
