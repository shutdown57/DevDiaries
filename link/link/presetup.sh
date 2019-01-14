#!/bin/sh

# export environment variables
# export $(grep -v '^#' ./.env | xargs -d '\n')
# export $(grep -v '^#' .env | xargs -d '\n')
export $(grep -v '^#' .env | xargs)

# initialize database
python ./manage.py db init
python ./manage.py init_db
python ./manage.py db upgrade

gunicorn wsgi -w 1 -b 0.0.0.0:5000 --reload
