from rest_framework import serializers
from .models import AcademicYear, CourseType, CourseCategory, CourseSubcategory, CourseStream, OrganizationType, \
    CollegeType


# Academic Year
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'


# Organization
class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = '__all__'


# CollegeType
class CollegeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeType
        fields = '__all__'


# CourseType
class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'


# CourseCategory
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


# basic Course category
class SimpleAcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        exclude = ('created_at','updated_at',)


# Organization
class SimpleOrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        exclude = ('created_at','updated_at',)


# CollegeType
class SimpleCollegeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeType
        exclude = ('created_at','updated_at',)


class SimpleCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('id', 'name','image',)


# Basic CourseType
class SimpleCourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = ('id', 'name',)


# CourseSubcategory
class CourseSubcategorySerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    type = SimpleCourseTypeSerializer(read_only=True)

    class Meta:
        model = CourseSubcategory
        fields = '__all__'


# Basic Coursesubcategory
class SimpleCourseSubcategorySerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    class Meta:
        model = CourseSubcategory
        exclude = ('created_at', 'updated_at',)


# CourseStream
class CourseStreamSerializer(serializers.ModelSerializer):
    course_subcategory = SimpleCourseSubcategorySerializer(read_only=True)
    class Meta:
        model = CourseStream
        fields = '__all__'
# ONLY Single

class OnlyCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('id', 'name','image',)
        
class OnlyCourseSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubcategory
        fields = ('id', 'course_name',)
        
class OnlyCourseStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStream
        fields = ('id', 'name',)
