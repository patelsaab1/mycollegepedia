import django_filters

from College.models import CourseFee, College


class CollegeFilter(django_filters.FilterSet):
    organization_type = django_filters.CharFilter(field_name='organization_type__name', lookup_expr='iexact')
    college_type = django_filters.CharFilter(field_name='college_type__name', lookup_expr='iexact')
    course_category = django_filters.CharFilter(field_name='course_category__name', lookup_expr='iexact')
    state = django_filters.CharFilter(field_name='state__name', lookup_expr='iexact')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='iexact')
    exam = django_filters.CharFilter(field_name='eligibility__exam__title', lookup_expr='iexact')
    rating = django_filters.CharFilter(field_name='rating', lookup_expr='iexact')
    
    class Meta:
        model = College
        fields = ['organization_type', 'college_type', 'course_category', 'state','country','exam','rating']


class CourseFeeFilter(django_filters.FilterSet):
    min_year_fees = django_filters.NumberFilter(field_name='year_fees', lookup_expr='gte')
    max_year_fees = django_filters.NumberFilter(field_name='year_fees', lookup_expr='lte')

    class Meta:
        model = CourseFee
        fields = ['min_year_fees', 'max_year_fees']
