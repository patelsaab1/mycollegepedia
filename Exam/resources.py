from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.core.exceptions import ValidationError

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
            raise ValidationError(
                f"{self.model._meta.verbose_name} not found: '{val}'. "
                "Pehle list me ye name create karo / exact spelling use karo."
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

    def before_import_row(self, row, row_number=None, **kwargs):
        for key in list(row.keys()):
            if key is None:
                continue
            nk = str(key).strip().lower()
            if nk != key:
                row[nk] = row.pop(key)
        if not str(row.get("title") or "").strip():
            raise ValidationError("Required: title (e.g. NEET UG)")
        cat = str(row.get("course_category") or "").strip()
        if cat and not CourseCategory.objects.filter(name__iexact=cat).exists():
            raise ValidationError(
                f"course_category '{cat}' not found. Use Medical / Engineering / "
                "Management / Law / Paramedical (run seed_masters if empty)."
            )


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

    def before_import_row(self, row, row_number=None, **kwargs):
        for key in list(row.keys()):
            if key is None:
                continue
            nk = str(key).strip().lower()
            if nk != key:
                row[nk] = row.pop(key)
        if not str(row.get("exam") or "").strip():
            raise ValidationError("Required: exam (= Exam title, e.g. NEET UG)")
        if not str(row.get("title") or "").strip():
            raise ValidationError("Required: title (e.g. NEET UG 2026)")
        mode = str(row.get("exam_mode") or "Online").strip()
        if mode and mode not in ("Online", "Offline"):
            raise ValidationError("exam_mode must be Online or Offline")
        row["exam_mode"] = mode or "Online"
