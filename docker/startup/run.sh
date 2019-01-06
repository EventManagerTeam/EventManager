#!/bin/bash
if [ -n "$GROUP_ID" -a -n "$GROUP_NAME" -a -n "$USER_ID" -a -n "$USER_NAME" ]; then
    addgroup -g $GROUP_ID $GROUP_NAME
    adduser -D -u $USER_ID $USER_NAME -G $GROUP_NAME
fi

python /code/eventmanager/manage.py migrate
python /code/eventmanager/manage.py loaddata /code/eventmanager/initial_categories.json
python /code/eventmanager/manage.py collectstatic --no-input
python /code/eventmanager/manage.py runserver 0.0.0.0:8000  

tail -f /dev/null