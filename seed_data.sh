#!/bin/bash

rm -rf stresslessapi/migrations
rm db.sqlite3
python manage.py makemigrations stresslessapi
python manage.py migrate
# load first three in order
python manage.py loaddata users
python manage.py loaddata tokens
# replace customers with app_users
python manage.py loaddata customers
# replace data tables with app models
python manage.py loaddata product_category
python manage.py loaddata product
python manage.py loaddata customerproductlike
python manage.py loaddata productrating
python manage.py loaddata payment
python manage.py loaddata order
python manage.py loaddata order_product
python manage.py loaddata favoritesellers