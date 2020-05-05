#!/bin/bash

set -o allexport
source /root/.env
set +o allexport

mkdir -pv /var/log/uwsgi /static

cd "$PIRADIO" && \
{
  python3 manage.py compress --extension=pug --force
  python3 manage.py collectstatic --no-input
}

