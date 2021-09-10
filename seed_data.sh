#!/bin/bash

rm -rf stresslessapi/migrations
rm db.sqlite3
python manage.py makemigrations stresslessapi
python manage.py migrate
# load first three in order
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata appUser
# replace data tables with app models
python manage.py loaddata reflection
python manage.py loaddata priority
python manage.py loaddata resources
python manage.py loaddata motivation
python manage.py loaddata post
python manage.py loaddata comment
python manage.py loaddata reaction
python manage.py loaddata postreaction