from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django import forms
from .forms import CustomUserCreationForm, CustomCollegeAdminForm, ChangeCollegeAdminForm,CounsellorAdmin,ChangeCounsellorAdminForm,CustomCounsellorAdminForm
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    resource_class = User
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'profile', 'name', 'email', 'mobile', 'dob', 'gender', 'religion', 'category',),
        }),
        ('User Credential', {
            'fields': ( 'is_superuser', 'is_staff', 'is_active','is_student','is_college','is_counsellor'),
        }),
        ('Address', {
            'fields': ('country', 'state', 'city', 'current_address', 'permanent_address','zipcode'),

        }),
        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),
    )

    def _profile(self, obj):
        return format_html('<img src="{}" style="max-width:150px; max-height:150px"/>'.format(obj.profile.url))

    list_display = ['name', 'email', 'mobile', 'gender', 'dob', 'country','date_joined']
    list_filter = ('dob', 'country', 'state', 'gender','date_joined')
    readonly_fields = ('last_login', 'date_joined',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "User Credential", "Address", "Login Info",)


@admin.register(CollegeAdmin)
class CollegeAdmin(admin.ModelAdmin):
    resource_class = CollegeAdmin
    change_form = ChangeCollegeAdminForm
    add_form = CustomCollegeAdminForm

    def _profile(self, obj):
        return format_html('<img src="{}" style="max-width:150px; max-height:150px"/>'.format(obj.profile.url))

    list_display = [ 'name','get_college_rank', 'email', 'mobile', 'gender', 'dob', 'country', 'department', 'designation', ]
    
    def get_college_rank(self, obj):
        return obj.college.rank if obj.college else None 
    get_college_rank.short_description = 'College Rank'
    
    list_filter = ('dob', 'country', 'state', 'gender',)
    ordering = ('-id',)
    # search_fields = (
    #     'name', 'email', 'mobile', 'country', 'state', 'city', 'zipcode', 'religion', 'category', 'department',
    #     'designation',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "User Credential", "Address", "Login Info",)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(CollegeAdmin, self).get_form(request, obj, **kwargs)
        
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('is_staff','groups',)
        return super().get_readonly_fields(request, obj)
        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(email=request.user.email)
        return qs

class EducationInline(admin.StackedInline):
    model = Education
    extra = 1


@admin.register(Student)
class StudentUserAdmin(admin.ModelAdmin):
    inlines = [EducationInline]
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'profile', 'name', 'email', 'mobile', 'dob', 'gender', 'religion', 'category',
                'course_interest',),
        }),
        ('User Credential', {
            'fields': ('is_active','is_student'),
        }),
        ('Address', {
            'fields': ('country', 'state', 'city', 'current_address', 'permanent_address','zipcode'),
        }),
        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),
    )
    list_display = ('name', 'email', 'mobile', 'course_interest',)
    list_filter = ('dob', 'country', 'state', 'gender', 'course_interest',)
    readonly_fields = ('last_login', 'date_joined',)
    # search_fields = ('name', 'email', 'mobile', 'course_interest', 'country', 'state', 'city', 'zipcode')
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Educations","User Credential", "Address", "Login Info",)


# @admin.register(Education)
# class EducationAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Basic Info', {
#             'fields': (
#                 'user', 'institute', 'degree', 'grade_system', 'score', 'field_of_study', 'start_date', 'end_date'),
#         }),
#     )
#     list_display = ('user', 'institute', 'degree', 'grade_system', 'score', 'field_of_study', 'start_date', 'end_date')
#     search_fields = ('user__email', 'institute', 'degree', 'field_of_study')


# admin.site.unregister(Group)

@admin.register(CounsellorAdmin)
class CounsellorAdmin(admin.ModelAdmin):
    # resource_class = CounsellorAdmin

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'profile', 'name', 'email', 'mobile', 'dob', 'gender', 'religion', 'category',),
        }),
        ('Company Basic Info', {
            'fields': (
                'brand_name', ),
        }),
        ('User Credential', {
            'fields': ('is_active', 'is_counsellor'),
        }),
        ('Login Info', {
            'fields': ('last_login', 'date_joined', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'profile', 'name', 'email', 'mobile', 'gender', 'dob', 'religion', 'category', 'brand_name', 'is_active', 'is_counsellor', 'password1', 'password2',),
        }
         ),
    )

    def _profile(self, obj):
        return format_html('<img src="{}" style="max-width:150px; max-height:150px"/>'.format(obj.profile.url))

    list_display = ['name', 'email', 'mobile', 'gender', 'dob', 'country', 'brand_name',]

    actions = ['approve_counsellor', 'reject_counsellor']

    list_filter = ('dob', 'gender', 'is_active')
    ordering = ('-id',)
    list_per_page = 10
    jazzmin_section_order = ("Basic Info", "Company Basic Info", "User Credential", "Address", "Login Info",)

    def approve_counsellor(self, request, queryset):
        for counsellor in queryset:
            counsellor.is_active = True
            counsellor.save()
            send_approve_counsellor_sms(counsellor)
        self.message_user(request, 'Selected counsellors approved successfully')

    def reject_counsellor(self, request, queryset):
        for counsellor in queryset:
            counsellor.is_active = False
            counsellor.save()
        self.message_user(request, 'Selected counsellors rejected successfully')

    approve_counsellor.short_description = 'Approve selected counsellor'
    reject_counsellor.short_description = 'Reject selected counsellor'

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('is_staff', 'groups',)
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(email=request.user.email)
        return qs

