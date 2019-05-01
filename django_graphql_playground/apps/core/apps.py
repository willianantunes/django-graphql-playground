from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "django_graphql_playground.apps.core"

    def ready(self):
        import django_graphql_playground.apps.core.signals
