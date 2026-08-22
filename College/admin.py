from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.utils.html import strip_tags
from django import forms
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
class FAQInline(admin.StackedInline):
    model = FAQ
    extra = 1

class CourseFeeInline(admin.StackedInline):
    model = CourseFee
    extra = 1

class CollegeVideoInline(admin.StackedInline):
    model = CollegeVideo
    extra = 1
    
class CollegeGalleryInline(admin.StackedInline):
    model = CollegeGallery
    extra = 1

@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [CollegeGalleryInline,CollegeVideoInline,CourseFeeInline,FAQInline]
    resource_classes = [CollegeResource]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('college_user', 'name', 'affiliation', 'rank', 'rating', 'logo', 'image', 'college_type',
                       'established_year', 'organization_type',
                       'course_category', 'course_subcategory', 'overview','views'),
        }),
        ('Admission Process', {
            'fields': ('admission_process',),
        }),
        ('Specialization', {
            'fields': ('specialization',),
        }),
        ('Career & Opportunity', {
            'fields': ('career_opportunity',),
        }),
        ('Placement', {
            'fields': ('placement',),
        }),
        ('Scholarship', {
            'fields': ('scholarship',),
        }),
        ('Scope', {
            'fields': ('scope',),
        }),
        ('Address', {
            'fields': ('country', 'state', 'city', 'current_address', 'permanent_address', 'zipcode'),
        }),
        ('Social Media', {
            'fields': (
            'primary_mobile', 'secondary_mobile', 'email', 'whatsapp', 'facebook', 'instagram', 'linkedin', 'twitter',
            'youtube', 'telegram','website'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description','slug'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def _logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.logo.url))
        else:
            return 'No logo'

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        else:
            return 'No image'

    list_display = ('name', 'college_user', 'college_type', 'established_year', 'rating', 'rank', '_logo', '_image','views')
    list_filter = ('name', 'college_type', 'established_year',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at','views')
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('college_user', 'rank', 'created_at', 'updated_at')
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college_user=request.user)
        return qs

    jazzmin_section_order = (
    "Basic Info", "Address", "Social Media","Awards & Achivements","Introductory Videos","Course Fees", "Admission Process", "Specialization", "Career & Opportunity", "Placement",
    "Scholarship", "Scope", "FAQs", "SEO", "Timestamp",)


class CollegeGalleryAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    fieldsets = (
        ('Basic Info', {
            'fields': ('college', 'image', 'title', 'alt', 'description',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:150px; max-height:150px"/>'.format(obj.image.url))
        else:
            return 'No image'

    list_display = ('college', '_image', 'title', 'alt', 'description',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('college__name', 'title',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college__college_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.college = request.user.collegeadmin.college
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)

admin.site.register(CollegeGallery, CollegeGalleryAdmin)

@admin.register(CollegeVideo)
class CollegeVideoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('college','title','videourl',  'alt', 'description',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
        )
            
    list_display = ('college', 'title', 'alt', 'description',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('college', 'title',)
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college__college_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.college = request.user.collegeadmin.college
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)


@admin.register(CourseFee)
class CourseFeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('college', 'academic_year', 'course_category',  'course_subcategory','course_stream', 'year_fees', 'total_fees',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
        )

    list_display = ('college', 'academic_year', 'course_subcategory', 'course_stream','year_fees', 'total_fees',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'total_fees')
    # search_fields = ('college__name','course_subcategory__name','course_stream__name', 'year_fees', 'total_fees')
    list_filter = ('college', 'course_subcategory', 'course_stream',)
    list_per_page=10
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college__college_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.college = request.user.collegeadmin.college
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)
    
@admin.register(CollegeApplication)
class CollegeApplicationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('student', 'college', 'course_category', 'course_subcategory', 'course_stream',
                'status'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('student', 'college', 'course_category', 'course_subcategory', 'course_stream', 'status')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('course_category', 'course_subcategory', 'course_stream', 'status',)
    search_fields = ('status', 'course_category', 'course_subcategory', 'course_stream',)
    list_per_page=10
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college__college_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.college = request.user.collegeadmin.college
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)

@admin.register(Eligibility)
class EligibilityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('college','exam', 'category','course_subcategory', 'course_stream','eligibility', 'description', 'application_start_date',
                'application_end_date'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('exam','college','category', 'course_subcategory','course_stream','truncated_eligibility', 'application_start_date', 'application_end_date')
   
    def truncated_eligibility(self, obj):
        return strip_tags(obj.eligibility)[:50] + '...' if obj.eligibility else ''
        
        
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('exam','college', 'course_subcategory', 'eligibility', 'application_start_date', 'application_end_date')
    list_per_page=10
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college__college_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.college = request.user.collegeadmin.college
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)
    
@admin.register(FAQ)
class FAQAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'college', 'question', 'answer',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )
    

    list_display = ('college', 'question', 'truncated_answer','created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('question', 'answer',)
    list_per_page=10
    def truncated_answer(self, obj):
        # Display the first 20 characters of the stripped answer
        return strip_tags(obj.answer)[:20] + '...' if obj.answer else ''
    
    truncated_answer.short_description = 'Answer'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(college__college_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.college = request.user.collegeadmin.college
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)
    
@admin.register(CollegeNews)
class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'college', 'course_category', 'title','image', 'post', 'status','views'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )
    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:150px; max-height:150px"/>'.format(obj.image.url))
        else:
            return 'No image'

    list_display = ('user', 'college', 'course_category', 'title','_image', 'status','views')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('user', 'course_category', 'college', 'status',)
    search_fields = ('title',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if not obj and request.user.is_staff and not request.user.is_superuser:
                form.base_fields['user'].initial = request.user
                form.base_fields['user'].widget = forms.HiddenInput()
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
            else:
                form.base_fields['user'].initial = request.user
                form.base_fields['user'].widget = forms.HiddenInput()
                form.base_fields['college'].initial = request.user.collegeadmin.college
                form.base_fields['college'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)
