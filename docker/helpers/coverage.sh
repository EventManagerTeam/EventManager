cd /code/eventmanager
coverage run manage.py test -v 2
coverage report -m --omit eventmanager/slugify.py
coverage html
