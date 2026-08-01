from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('year', 'status'),

        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('year', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('year', 'status',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Timestamp",)


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name',),

        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Timestamp",)


@admin.register(CollegeType)
class CollegeTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name',),

        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Timestamp",)


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Timestamp",)


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name','image'),

        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',),
        }),
    )
    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:60px; max-height:60px"/>'.format(obj.image.url))
        else:
            return 'No image'
    list_display = ('name','_image','created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Timestamp",)


class CourseStreamInline(admin.StackedInline):
    model = CourseStream
    extra = 1


@admin.register(CourseSubcategory)
class CourseSubcategoryAdmin(admin.ModelAdmin):
    inlines = [CourseStreamInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('course_category', 'type', 'course_name', 'exam_type', 'duration', 'semester', 'description'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',),
        }),
    )

    list_display = (
        'course_category', 'type', 'course_name', 'exam_type', 'duration', 'semester', 'created_at', 'updated_at')
    list_filter = ('course_category', 'type', 'exam_type')
    readonly_fields = ('semester', 'created_at', 'updated_at')
    search_fields = (
        'course_category', 'type', 'course_name', 'exam_type', 'duration', 'semester', 'created_at', 'updated_at')
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Course Streams", "Timestamp",)


@admin.register(CourseStream)
class CourseStreamAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('course_subcategory', 'name'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('course_subcategory', 'name', 'created_at', 'updated_at')
    list_filter = ('course_subcategory',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('course_subcategory', 'name', 'created_at', 'updated_at')
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Timestamp",)
