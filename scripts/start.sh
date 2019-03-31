#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate

echo "Querying ADMIN table..."
count=$(echo "from django.contrib.auth import get_user_model;\
User = get_user_model();\
print(len(User.objects.all()))" | python manage.py shell)

echo "Admins configured: ${count}"

if [ ${count} -eq 0 ] ; then
    echo "Creating temporary ADMIN user..."
    echo "from django.contrib.auth import get_user_model;\
    User = get_user_model();\
    User.objects.create_superuser('admin', None, 'admin')" | python manage.py shell
fi


if [[ ${DJANGO_BIND_ADDRESS+x} ]] && [[ ${DJANGO_BIND_PORT+x} ]];
then
    echo "OK! Using custom ADRESSS $DJANGO_BIND_ADDRESS and PORT $DJANGO_BIND_PORT to set Django runserver command"
    python manage.py runserver ${DJANGO_BIND_ADDRESS}:${DJANGO_BIND_PORT}
else
    echo "Using 0.0.0.0:80 as parameter for Django runserver command"
    python manage.py runserver 0.0.0.0:80
fi
