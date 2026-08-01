from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.utils.html import strip_tags
from django import forms
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class DirectorInline(admin.StackedInline):
    model = Director
    extra = 1
    fields = ('organization_type', 'profile', 'name','id_proof','primary_mobile','secondary_mobile','email', 'whatsapp', 'facebook', 'instagram', 'linkedin', 'twitter', 'youtube', 'telegram') 

class FAQInline(admin.StackedInline):
    model = FAQ
    extra = 1

@admin.register(Counsellor)
class CounsellorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [DirectorInline,FAQInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('counsellor_user', 'company_name', 'area_of_operation', 'logo', 'image', 'registration_date','primary_mobile', 'secondary_mobile','gst','pan_no','pan_card','company_certificate'),
        }),
        ('Overview', {
            'fields': ('overview',),
        }),
        ('Success Story', {
            'fields': ('success_story',),
        }),
        ('Address', {
            'fields': ('country', 'state', 'city', 'current_address', 'permanent_address', 'zipcode'),
        }),
        ('Social Media', {
            'fields': ('email', 'whatsapp', 'facebook', 'instagram', 'linkedin', 'twitter', 'youtube', 'telegram','website'),
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

    list_display = ('counsellor_user', 'company_name','gst', '_logo', '_image')
    list_filter = ('counsellor_user', 'company_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        # If the user is not a superuser, return a tuple of read-only fields
        if not request.user.is_superuser:
            return ('counsellor_user', 'created_at', 'updated_at')
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(counsellor_user=request.user)
        return qs

    jazzmin_section_order = ("Basic Info", "Overview", "Success Story", "Social Media", "Address", "Directors", "SEO","FAQs", "Timestamp",)

admin.site.register(OrganizationType)

@admin.register(Director)
class DirectorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('counsellor', 'organization_type', 'profile', 'name', 'primary_mobile', 'secondary_mobile','identity', 'id_proof'),
        }),

        ('Social Media', {
            'fields': ('email', 'whatsapp', 'facebook', 'instagram', 'linkedin', 'twitter', 'youtube', 'telegram'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )


    def _profile(self, obj):
        if obj.profile:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.profile.url))
        else:
            return 'No profile'


    list_display = ('counsellor', 'name', 'organization_type', '_profile')
    list_filter = ('counsellor', 'name', 'organization_type')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_counsellor and not request.user.is_superuser:
            if obj is None:
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
        return form
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(counsellor__counsellor_user=request.user)
        return qs
    
    
    def save_model(self, request, obj, form, change):
        if not change and request.user.is_counsellor and not request.user.is_superuser:
            obj.counsellor = request.user.counselloradmin.counsellor
        super().save_model(request, obj, form, change)
    
    
    jazzmin_section_order = ("Basic Info", "Social Media", "Timestamp",)


@admin.register(CounsellorTestimonial)
class CounsellorTestimonialAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('counsellor', 'name', 'description', 'rating',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('counsellor', 'name', 'rating',)
    list_filter = ('counsellor', 'name', 'rating',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        # If the user is not a superuser, return a tuple of read-only fields
        if not request.user.is_superuser:
            return ('counsellor', 'created_at', 'updated_at')
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(counsellor=request.user)
        return qs

    jazzmin_section_order = ("Basic Info", "Timestamp",)
    
    
    
@admin.register(Leads)
class LeadsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('student', 'counsellor', 'course_category', 'course_subcategory', 'course_stream',
                'status'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('student', 'counsellor', 'course_category', 'course_subcategory', 'course_stream', 'status')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('course_category', 'course_subcategory', 'course_stream', 'status',)
    search_fields = ('status', 'course_category', 'course_subcategory', 'course_stream',)
    list_per_page=10
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(counsellor__counsellor_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_counsellor and not request.user.is_superuser:
            obj.counsellor = request.user.counselloradmin.counsellor
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)
    
@admin.register(FAQ)
class FAQAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'counsellor', 'question', 'answer',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('counsellor', 'question', 'truncated_answer', 'created_at',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('question', 'answer',)
    list_per_page = 10

    def truncated_answer(self, obj):
        # Display the first 20 characters of the stripped answer
        return strip_tags(obj.answer)[:20] + '...' if obj.answer else ''

    truncated_answer.short_description = 'Answer'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if obj is None:
                # For new entries, set initial value and hide the field
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
            else:
                # For existing entries, display the field as read-only
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(counsellor__counsellor_user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_staff and not request.user.is_superuser:
            obj.counsellor = request.user.counselloradmin.counsellor
        super().save_model(request, obj, form, change)

    jazzmin_section_order = ("Basic Info", "Timestamp",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'counsellor', 'course_category', 'title','image', 'post', 'status','views'),
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

    list_display = ('user', 'counsellor', 'course_category', 'title','_image', 'status','views')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('user', 'course_category', 'counsellor', 'status',)
    search_fields = ('title',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_staff and not request.user.is_superuser:
            if not obj and request.user.is_staff and not request.user.is_superuser:
                form.base_fields['user'].initial = request.user
                form.base_fields['user'].widget = forms.HiddenInput()
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
            else:
                form.base_fields['user'].initial = request.user
                form.base_fields['user'].widget = forms.HiddenInput()
                form.base_fields['counsellor'].initial = request.user.counselloradmin.counsellor
                form.base_fields['counsellor'].widget = forms.HiddenInput()
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