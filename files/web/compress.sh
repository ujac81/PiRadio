#!/bin/bash


#grep "=" /root/.env | while read line; do
#  var=`echo $line | cut -d= -f1`
#  val=`echo $line | cut -d= -f2`
#  export $var="$val"
#done

set -o allexport
source /root/.env
set +o allexport

env

cd "$PIRADIO"
pwd
python3 manage.py compress --extension=pug --force
python3 manage.py collectstatic --no-input

