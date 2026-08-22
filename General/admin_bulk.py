"""Admin mixin: Download Excel Template button on changelist."""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html

from General.bulk_templates import build_template_bytes


class BulkTemplateDownloadMixin:
    """
    Set on ModelAdmin:
      bulk_template_key = 'exam'  # college | exam | upcoming_exam
    """
    bulk_template_key = None

    def get_urls(self):
        urls = super().get_urls()
        if not self.bulk_template_key:
            return urls
        custom = [
            path(
                "download-bulk-template/",
                self.admin_site.admin_view(self.download_bulk_template),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_bulk_template",
            ),
        ]
        return custom + urls

    def download_bulk_template(self, request):
        filename, data = build_template_bytes(self.bulk_template_key)
        response = HttpResponse(
            data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def bulk_template_button(self):
        if not self.bulk_template_key:
            return ""
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_bulk_template"
        )
        return format_html(
            '<a class="btn btn-success" href="{}" style="margin-right:8px;">'
            "Download Excel Template</a>",
            url,
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["bulk_template_button"] = self.bulk_template_button()
        return super().changelist_view(request, extra_context=extra_context)


# Minimal changelist override: inject button above object-tools via Jazzmin-friendly template
class BulkTemplateAdmin(BulkTemplateDownloadMixin, admin.ModelAdmin):
    change_list_template = "admin/bulk_import_change_list.html"
