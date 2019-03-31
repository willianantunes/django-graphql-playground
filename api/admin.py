from django.contrib import admin

from api.models import Category
from api.models import Ingredient
from api.support.admin_services import CustomModelAdminMixin
from api.support.admin_services import ExportCsvMixin


@admin.register(Category)
class CategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    list_filter = ["created_at", "updated_at"]
    actions = ["export_as_csv"]


@admin.register(Ingredient)
class IngredientAdmin(CustomModelAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    list_filter = ["category", "created_at", "updated_at"]
    raw_id_fields = ["category"]
    actions = ["export_as_csv"]
