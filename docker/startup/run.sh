#!/bin/bash
if [ -n "$GROUP_ID" -a -n "$GROUP_NAME" -a -n "$USER_ID" -a -n "$USER_NAME" ]; then
    addgroup -g $GROUP_ID $GROUP_NAME
    adduser -D -u $USER_ID $USER_NAME -G $GROUP_NAME
fi

[ -e /tmp/worker.pid ] && rm /tmp/worker.pid
[ -e /tmp/celerybeat.pid ] && rm /tmp/celerybeat.pid

python3.6 /code/webapp/manage.py migrate --settings=webapp.env.local_settings
python3.6 /code/webapp/manage.py loaddata --settings=webapp.env.local_settings initial_user
python3.6 /code/webapp/manage.py collectstatic --no-input

cd /code/webapp && celery multi start -A webapp worker -l info --pidfile=/tmp/worker.pid --concurrency=5 -n worker@%h --logfile="/tmp/%n%I.log"
cd /code/webapp && celery -A webapp beat -l info -S django --pidfile=/tmp/celerybeat.pid --logfile="/tmp/%n%I.log" --detach

python3.6 /code/webapp/manage.py runserver 0.0.0.0:8000 --settings="webapp.env.local_settings"
