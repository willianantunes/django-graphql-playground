"""django_graphql_playground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.authtoken import views as drf_auth_views

from api.drf.views import CategoryViewSet
from api.drf.views import IngredientViewSet
from api.graphql.schema import schema
from api.graphql.views import DRFAuthenticatedGraphQLView

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"ingredients", IngredientViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/auth-token/", drf_auth_views.obtain_auth_token),
    path("api/graphql/", csrf_exempt(DRFAuthenticatedGraphQLView.as_view(graphiql=True, schema=schema))),
]
