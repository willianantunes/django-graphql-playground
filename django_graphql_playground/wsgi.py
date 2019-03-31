"""
WSGI config for django_graphql_playground project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

from django_graphql_playground import settings
from django_graphql_playground.settings import Enviroments

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_graphql_playground.settings")

application = get_wsgi_application()


if settings.ENVIRONMENT == Enviroments.DEV.name:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
