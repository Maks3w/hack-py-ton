#!/usr/bin/env sh

python manage.py migrate \
  && exec python manage.py runserver 0.0.0.0:"${SERVER_PORT}"
