import csv
import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)


class CustomModelAdminMixin:
    def __init__(self, model, admin_site):
        if self.list_display and self.list_display[0] == "__str__":
            self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        if not self.list_filter:
            self.list_filter = [field.name for field in model._meta.fields if field.name != "id"]
        if not self.readonly_fields:
            self.readonly_fields = ["created_at", "updated_at"]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        translation_callable = lambda writer, instance, field_names: writer.writerow(
            [getattr(obj, field) for field in field_names]
        )
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        logger.info(f"Export CSV to {meta} with the follwing fields: {field_names}")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)

        if hasattr(self, "custom_csv_row_translation") and self.custom_csv_row_translation:
            translation_callable = self.custom_csv_row_translation

        for obj in queryset:
            translation_callable(writer, obj, field_names)

        return response

    export_as_csv.short_description = "Export CSV"
