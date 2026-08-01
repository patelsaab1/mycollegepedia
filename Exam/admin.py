from django.contrib import admin
from django.utils.html import format_html
from Exam.models import Exam, UpcomingExam


# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('course_category','title', 'image','full_form',),
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
        else:
            return 'No image'

    list_display = ('title','_image','course_category','full_form', 'created_at', 'updated_at',)
    list_filter = ('title', 'full_form','course_category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'full_form',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Description","SEO", "Timestamp",)


@admin.register(UpcomingExam)
class UpcomingExamAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('exam', 'title', 'exam_mode',  'exam_start_date', 'exam_end_date', 'application_start_date',
                       'application_end_date', 'result', 'url'),
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

    list_display = ('title','exam', 'exam_mode', 'exam_start_date', 'exam_end_date', 'application_start_date',
        'application_end_date',
        'result',)
    list_filter = ('exam_mode', 'exam_start_date', 'exam_end_date',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('exam_mode', 'exam_start_date', 'exam_end_date',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Description","SEO", "Timestamp",)




# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Basic Info', {
#             'fields': ('course_category','title', 'image','full_form',),
#         }),
#         ('Description', {
#             'fields': ('description',),
#         }),
        
#         ('Timestamp', {
#             'fields': ('created_at', 'updated_at',),
#         }),
#     )
#     def _image(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" style="max-width:60px; max-height:60px"/>'.format(obj.image.url))
#         else:
#             return 'No image'

#     list_display = ('title','_image','full_form', 'created_at', 'updated_at',)
#     list_filter = ('title', 'full_form','course_category',)
#     ordering = ('-created_at',)
#     readonly_fields = ('created_at', 'updated_at')
#     search_fields = ('title', 'full_form',)
#     list_per_page=10
#     jazzmin_section_order = ("Basic Info", "Description", "SEO","Timestamp",)


# @admin.register(UpcomingExam)
# class UpcomingExamAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Basic Info', {
#             'fields': ('exam', 'title', 'exam_mode',  'exam_start_date', 'exam_end_date', 'application_start_date',
#                       'application_end_date', 'result', 'url'),
#         }),
#         ('Description', {
#             'fields': ('description',),
#         }),
#         ('SEO', {
#             'fields': ('title', 'keyword', 'description', ),
#         }),
#         ('Timestamp', {
#             'fields': ('created_at', 'updated_at',),
#         }),
#     )

#     list_display = ('title','exam', 'exam_mode', 'exam_start_date', 'exam_end_date', 'application_start_date',
#         'application_end_date',
#         'result',)
#     list_filter = ('exam_mode', 'exam_start_date', 'exam_end_date',)
#     ordering = ('-created_at',)
#     readonly_fields = ('created_at', 'updated_at')
#     search_fields = ('exam_mode', 'exam_start_date', 'exam_end_date',)
#     list_per_page=10
#     jazzmin_section_order = ("Basic Info", "Description", "SEO","Timestamp",)
