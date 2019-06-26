from django.contrib import admin
from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient
from django_graphql_playground.support.django_helpers import CustomModelAdminMixin
from django_graphql_playground.support.django_helpers import ExportCsvMixin


@admin.register(Category)
class CategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]


@admin.register(Ingredient)
class IngredientAdmin(CustomModelAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    list_filter = ["category", "created_at", "updated_at"]
    actions = ["export_as_csv"]
