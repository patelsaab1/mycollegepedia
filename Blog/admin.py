from django.contrib import admin
from .models import Blog, Tag,Comment
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .resources import BlogResource

# Register your models here.
class TagInline(admin.StackedInline):
    model = Tag
    extra = 1
    
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    readonly_fields = ['user', 'blog', 'text', 'created_at']


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [TagInline,CommentInline]
    resource_classes = [BlogResource]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('author', 'category', 'title', 'image', 'post', 'status',),
        }),
         ('SEO', {
            'fields': ('meta_title', 'meta_keyword', 'meta_description','slug' ),
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at','published_date','views',),
        }),
    )

    def _image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        else:
            return 'No image'
    
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('author', '_image', 'title', 'category', 'status','views',)
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('author', 'category', 'status','published_date',)
    search_fields = ('user', 'title', 'category','published_date','views')
    list_per_page=10
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj and request.user.is_staff and not request.user.is_superuser:
            form.base_fields['author'].initial = request.user
            form.base_fields['author'].widget.attrs['disabled'] = True
            form.base_fields['published_date'].widget.attrs['disabled'] = True
            form.base_fields['views'].widget.attrs['disabled'] = True
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(author=request.user)
        return qs

    jazzmin_section_order = ("Basic Info", "Tags", "SEO", "Comments","Timestamp",)

admin.site.register(Tag)
