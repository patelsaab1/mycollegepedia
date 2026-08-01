from django_filters import rest_framework as filters

from .models import Blog

class BlogListFilter(filters.FilterSet):
    class Meta:
        model = Blog
        fields = {'category': ['exact']}