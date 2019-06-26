import csv
from enum import Enum

from django.db import connection
from django.db import connections
from django.db.models import ForeignKey
from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        translation_callable = lambda writer, instance, field_names: writer.writerow(
            [getattr(obj, field) for field in field_names]
        )
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

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


class CustomModelAdminMixin:
    def __init__(self, model, admin_site):
        if self.list_display and self.list_display[0] == "__str__":
            self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        if not self.list_filter:
            self.list_filter = ["created_at", "updated_at"]
        if not self.readonly_fields:
            self.readonly_fields = ["created_at", "updated_at"]
        if not self.raw_id_fields:
            # Only for FOREIGN KEY fields
            raw_id_fields = []
            for key, value in model._meta._forward_fields_map.items():
                if type(value) is ForeignKey and not key.endswith("id"):
                    raw_id_fields.append(key)
            if raw_id_fields:
                self.raw_id_fields = raw_id_fields
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


def batch_qs(query_set, batch_size=1000):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.

    Usage:
        # Make sure to order your querset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = query_set.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, query_set[start:end])


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)

    @classmethod
    def name_from_value(cls, value):
        for name, v in cls.choices():
            if value == v:
                return name


def make_sure_database_is_usable():
    """
    https://github.com/speedocjx/db_platform/blob/e626a12edf8aceb299686fe19377cd6ff331b530/myapp/include/inception.py#L14
    """
    if connection.connection and not connection.is_usable():
        """
        Database might be lazily connected to in django.
        When connection.connection is None means you have not connected to mysql before.        
        Destroy the default mysql connection after this line, 
        when you use ORM methods django will reconnect to the default database
        """
        del connections._connections.default
