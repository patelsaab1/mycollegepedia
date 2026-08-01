from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .filters import CourseSubcategoryFilter, CourseStreamFilter
from .models import AcademicYear, CourseType, CourseCategory, CourseSubcategory, CourseStream, OrganizationType, \
    CollegeType
from .permissions import IsSuperuser
from .serializers import AcademicYearSerializer, CourseTypeSerializer, CourseCategorySerializer, \
    CourseSubcategorySerializer, CourseStreamSerializer, OrganizationTypeSerializer, CollegeTypeSerializer,OnlyCourseSubcategorySerializer,OnlyCourseCategorySerializer, OnlyCourseStreamSerializer,SimpleCourseSubcategorySerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


# Basic
class AcademicYearRetrieveView(generics.RetrieveAPIView):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    # permission_classes = (IsAuthenticated,)

class CourseCategoryListView(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = OnlyCourseCategorySerializer
    
class CourseSubcategoryListView(generics.ListAPIView):
    queryset = CourseSubcategory.objects.all()
    serializer_class = OnlyCourseSubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseSubcategoryFilter

class CourseStreamListView(generics.ListAPIView):
    queryset = CourseStream.objects.all()
    serializer_class = OnlyCourseStreamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseStreamFilter

# SuperUser Access Only
class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['year', 'status']


class OrganizationTypeViewSet(viewsets.ModelViewSet):
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer
    permission_classes = [IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CollegeTypeViewSet(viewsets.ModelViewSet):
    queryset = CollegeType.objects.all()
    serializer_class = CollegeTypeSerializer
    permission_classes = [IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CourseTypeViewSet(viewsets.ModelViewSet):
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CourseSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseSubcategory.objects.all()
    serializer_class = CourseSubcategorySerializer
    permission_classes = [IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['course_category', 'type', 'course_name', 'exam_type', 'duration', 'semester']


class CourseStreamViewSet(viewsets.ModelViewSet):
    queryset = CourseStream.objects.all()
    serializer_class = CourseStreamSerializer
    permission_classes = [IsSuperuser]
    filter_backends = [SearchFilter]
    search_fields = ['course_subcategory', 'name']
    
