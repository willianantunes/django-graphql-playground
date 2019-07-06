#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_db --create-super-user

if [[ ${PORT+x} ]];
then
    echo "OK! Using custom PORT $PORT to set Django runserver command"
    python manage.py runserver 0.0.0.0:${PORT}
else
    echo "Using 0.0.0.0:8000 as parameter for Django runserver command"
    python manage.py runserver 0.0.0.0:8000
fi
