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
    echo "Done!"
fi

python manage.py runserver ${DJANGO_BIND_ADDRESS}:${DJANGO_BIND_PORT}
