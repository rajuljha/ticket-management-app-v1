#!/bin/bash
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"rajuljha49@gmail.com"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --email ${SUPERUSER_EMAIL} --noinput || true
# THE || true is added so that the command runs more than one time without failing