import django_filters

from .models import *


class CourseSubcategoryFilter(django_filters.FilterSet):
    course_category = django_filters.CharFilter(field_name='course_category__name', lookup_expr='iexact')
    
    class Meta:
        model = CourseSubcategory
        fields = ['course_category', ]
        
class CourseStreamFilter(django_filters.FilterSet):
    course_subcategory = django_filters.CharFilter(field_name='course_subcategory__course_name', lookup_expr='iexact')
    
    class Meta:
        model = CourseStream
        fields = ['course_subcategory', ]