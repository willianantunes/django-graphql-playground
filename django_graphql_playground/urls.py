from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.authtoken import views as drf_auth_views

from django_graphql_playground.apps.drf.views import CategoryViewSet
from django_graphql_playground.apps.drf.views import IngredientViewSet
from django_graphql_playground.apps.gqyl.schema import schema
from django_graphql_playground.apps.gqyl.views import DRFAuthenticatedGraphQLView

admin.site.site_title = "Django GraphQL Playground"
admin.site.site_header = f"{admin.site.site_title} administration"
admin.site.index_title = f"Welcome to {admin.site.site_header} Portal"

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"ingredients", IngredientViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/auth-token/", drf_auth_views.obtain_auth_token),
    path("api/graphql/", csrf_exempt(DRFAuthenticatedGraphQLView.as_view(graphiql=True, schema=schema))),
]
