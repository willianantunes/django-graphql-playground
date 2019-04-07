from django.contrib import admin

from app.models import Category
from app.models import Ingredient
from app.support.admin_services import CustomModelAdminMixin
from app.support.admin_services import ExportCsvMixin


@admin.register(Category)
class CategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    list_filter = ["created_at", "updated_at"]
    actions = ["export_as_csv"]


@admin.register(Ingredient)
class IngredientAdmin(CustomModelAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    list_filter = ["category", "created_at", "updated_at"]
    raw_id_fields = ["category"]
    actions = ["export_as_csv"]
