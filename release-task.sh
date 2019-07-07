#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_db --create-super-user
