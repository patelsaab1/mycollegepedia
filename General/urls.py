from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AcademicYearViewSet,CourseTypeViewSet,CourseCategoryViewSet,CourseSubcategoryViewSet,CourseStreamViewSet,OrganizationTypeViewSet,CollegeTypeViewSet, CourseSubcategoryListView,CourseStreamListView,CourseCategoryListView,AcademicYearRetrieveView
router = DefaultRouter()
router.register(r'academic-year', AcademicYearViewSet, basename='academic-year')
router.register(r'organization-type', OrganizationTypeViewSet, basename='organization-type')
router.register(r'college-type', CollegeTypeViewSet, basename='college-type')
router.register(r'course-type', CourseTypeViewSet, basename='course-type')
router.register(r'course-category', CourseCategoryViewSet, basename='course-category')
router.register(r'course-subcategory', CourseSubcategoryViewSet, basename='course-subcategory')
router.register(r'course-stream', CourseStreamViewSet, basename='course-stream')
urlpatterns = [
    path('all_course_category/',CourseCategoryListView.as_view(),name="all_course_category"),
    path('academic/<int:pk>/',AcademicYearRetrieveView.as_view(),name="academic-year"),
    path('all_course_subcategory/',CourseSubcategoryListView.as_view(),name="all_course_subcategory"),
    path('all_course_stream/',CourseStreamListView.as_view(),name="all_course_stream"),
    path('', include(router.urls)),
]
