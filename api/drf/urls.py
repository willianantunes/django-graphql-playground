from rest_framework import routers

from api.drf import views


def build():
    router = routers.DefaultRouter()
    router.register(r"categories", views.CategoryViewSet)
    router.register(r"ingredients", views.IngredientViewSet)

    return router.urls
