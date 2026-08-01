from django.contrib import admin
from .models import SiteConfig, Slider, Contact, About,PrivacyPolicy,Testimonial,TermsAndCondition,Feedback,Experience
from django.utils.html import format_html, strip_tags


# Register your models here.
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title', 'favicon', 'logo', 'primary_mobile', 'secondary_mobile',),
        }),
        ('Social Info', {
            'fields': (
                'email', 'whatsapp', 'facebook','instagram','twitter','linkedin','youtube','playstore', 'appstore',),
        }),
        ('Description', {
            'fields': (
                'short_description',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', ),
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

    list_display = ('title', '_logo', 'email', 'primary_mobile',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'email', 'primary_mobile',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Social Info", "Description","SEO", "Timestamp",)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title', 'image', 'url',),
        }),
        ('Description', {
            'fields': (
                'short_description',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        else:
            return 'No logo'

    list_display = ('title', '_image', 'url')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Description", "Timestamp",)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title',),
        }),
        ('Description', {
            'fields': (
                'description',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', ),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('title', 'truncated_description')
    def truncated_description(self, obj):
       
        return strip_tags(obj.description)[:50] + '...' if obj.description else ''
    
    truncated_description.short_description = 'Description'
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Description","SEO", "Timestamp",)
    
@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title',),
        }),
        ('Description', {
            'fields': (
                'description',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', ),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )


    list_display = ('title', 'truncated_description')
    def truncated_description(self, obj):
       
        return strip_tags(obj.description)[:50] + '...' if obj.description else ''
    
    truncated_description.short_description = 'Description'
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Description","SEO", "Timestamp",)


@admin.register(TermsAndCondition)
class TermsAndConditionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title',),
        }),
        ('Description', {
            'fields': (
                'description',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description', ),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )



    list_display = ('title', 'truncated_description')
    def truncated_description(self, obj):
       
        return strip_tags(obj.description)[:50] + '...' if obj.description else ''
    
    truncated_description.short_description = 'Description'
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title',)
    list_per_page=10
    jazzmin_section_order = ("Basic Info", "Description","SEO", "Timestamp",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Message', {
            'fields': (
                'name', 'email', 'mobile', 'subject', 'message'),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('name', 'email', 'mobile', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page=10
    
    def has_add_permission(self, request):
        return False
        
    jazzmin_section_order = ("Message", "Timestamp",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'user','description','rating',),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    list_display = ('user', 'truncated_description','rating','created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page=10
    def truncated_description(self, obj):
        return strip_tags(obj.description)[:20] + '...' if obj.description else ''
    
    truncated_description.short_description = 'Description'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj and request.user.is_staff and not request.user.is_superuser:
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].widget.attrs['disabled'] = True
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs
    jazzmin_section_order = ("Basic Info", "Timestamp",)
    
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'phone','email', 'message', 'rating'),
        }),
        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )
    
    def truncated_description(self, obj):
       
        return strip_tags(obj.message)[:50] + '...' if obj.message else ''
    
    truncated_description.short_description = 'message'
    

    def rating_stars(self, obj):
        stars = '★' * obj.rating
        return format_html('<span style="color: orange;">{}</span>', stars)

    rating_stars.short_description = 'Rating'
    list_display = ['name', 'phone', 'email','truncated_description', 'rating_stars']
    list_filter = ('name', 'phone','email', 'rating', 'created_at', 'updated_at',)
    search_fields = ('name', 'phone','email')
    readonly_fields = ('name', 'phone', 'email','rating', 'message', 'created_at', 'updated_at',)
    list_per_page = 10
    
    def has_add_permission(self, request):
        return False
        
    
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('note', 'rating'),
        }),
        ('TimeStamp', {
            'fields': ('created_at', 'updated_at',),
        }),
    )
    
    def truncated_description(self, obj):
       
        return strip_tags(obj.note)[:50] + '...' if obj.note else ''
    
    truncated_description.short_description = 'note'
    

    def rating_stars(self, obj):
        stars = '★' * obj.rating
        return format_html('<span style="color: orange;">{}</span>', stars)

    rating_stars.short_description = 'Rating'
    list_display = ['truncated_description', 'rating_stars']
    list_filter = ( 'rating', 'created_at', 'updated_at',)
    readonly_fields = ('rating', 'note', 'created_at', 'updated_at',)
    list_per_page = 10
    
    def has_add_permission(self, request):
        return False