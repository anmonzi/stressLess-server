#!/bin/bash

rm -rf stresslessapi/migrations
rm db.sqlite3
python manage.py makemigrations stresslessapi
python manage.py migrate
# load first three in order
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata appUsers
# replace data tables with app models
python manage.py loaddata reflections
python manage.py loaddata priorities
python manage.py loaddata resources
python manage.py loaddata motivations
python manage.py loaddata posts
python manage.py loaddata comments
python manage.py loaddata reactions
python manage.py loaddata postreactions