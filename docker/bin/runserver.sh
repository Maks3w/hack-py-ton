#!/usr/bin/env sh

exec python manage.py runserver 0.0.0.0:"${SERVER_PORT}"
