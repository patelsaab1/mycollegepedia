from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from General.models import CourseCategory
from .models import Exam, UpcomingExam


class CaseInsensitiveNameWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        if value in (None, ""):
            return None
        val = str(value).strip()
        try:
            return self.get_queryset(value, row, **kwargs).get(**{f"{self.field}__iexact": val})
        except self.model.DoesNotExist as exc:
            from django.core.exceptions import ValidationError
            raise ValidationError(
                f"{self.model._meta.verbose_name} not found: {self.field}='{val}'"
            ) from exc


class ExamResource(resources.ModelResource):
    course_category = fields.Field(
        column_name="course_category",
        attribute="course_category",
        widget=CaseInsensitiveNameWidget(CourseCategory, "name"),
    )

    class Meta:
        model = Exam
        import_id_fields = ("title",)
        skip_unchanged = True
        report_skipped = True
        fields = (
            "title",
            "full_form",
            "course_category",
            "description",
            "meta_title",
            "meta_keyword",
            "meta_description",
            "slug",
        )
        export_order = fields


class UpcomingExamResource(resources.ModelResource):
    exam = fields.Field(
        column_name="exam",
        attribute="exam",
        widget=CaseInsensitiveNameWidget(Exam, "title"),
    )

    class Meta:
        model = UpcomingExam
        import_id_fields = ("title",)
        skip_unchanged = True
        report_skipped = True
        fields = (
            "exam",
            "title",
            "exam_mode",
            "description",
            "application_start_date",
            "application_end_date",
            "exam_start_date",
            "exam_end_date",
            "result",
            "url",
            "meta_title",
            "meta_keyword",
            "meta_description",
            "slug",
        )
        export_order = fields
