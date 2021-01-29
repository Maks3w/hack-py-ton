#!/usr/bin/env sh

python manage.py migrate \
  && python manage.py loaddata \
      core/fixtures/users.json \
  && exec python manage.py runserver 0.0.0.0:"${SERVER_PORT}"
