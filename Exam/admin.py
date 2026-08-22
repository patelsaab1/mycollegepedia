from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from Exam.models import Exam, UpcomingExam
from Exam.resources import ExamResource, UpcomingExamResource


@admin.register(Exam)
class ExamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ExamResource]
    fieldsets = (
        ('Basic Info', {
            'fields': ('course_category', 'title', 'image', 'full_form',),
            'description': (
                'Bulk upload: Export → template headers rakho → Import. '
                'Columns: title, full_form, course_category, description, meta_title, slug. '
                'course_category exact name (Medical, Engineering…).'
            ),
        }),
        ('Description', {
            'fields': ('description',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'slug'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:60px; max-height:60px"/>'.format(obj.image.url))
        return 'No image'

    list_display = ('title', '_image', 'course_category', 'full_form', 'created_at', 'updated_at',)
    list_filter = ('title', 'full_form', 'course_category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'full_form',)
    list_per_page = 10
    jazzmin_section_order = ("Basic Info", "Description", "SEO", "Timestamp",)


@admin.register(UpcomingExam)
class UpcomingExamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [UpcomingExamResource]
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'exam', 'title', 'exam_mode', 'exam_start_date', 'exam_end_date',
                'application_start_date', 'application_end_date', 'result', 'url',
            ),
            'description': (
                'Bulk: pehle Exam import karo. Upcoming sheet me exam = Exam title (e.g. NEET UG). '
                'Dates: YYYY-MM-DD. exam_mode: Online ya Offline.'
            ),
        }),
        ('Description', {
            'fields': ('description',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', 'slug'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = (
        'title', 'exam', 'exam_mode', 'exam_start_date', 'exam_end_date',
        'application_start_date', 'application_end_date', 'result',
    )
    list_filter = ('exam_mode', 'exam_start_date', 'exam_end_date',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'exam__title',)
    list_per_page = 10
    jazzmin_section_order = ("Basic Info", "Description", "SEO", "Timestamp",)
