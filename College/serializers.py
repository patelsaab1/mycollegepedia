from rest_framework import serializers
from College.models import College, CollegeGallery, CourseFee, Eligibility, CollegeApplication, FAQ, CollegeNews, CollegeVideo
from General.serializers import CourseCategorySerializer, CourseSubcategorySerializer, AcademicYearSerializer, CourseStreamSerializer
from General.serializers import *
from Exam.serializers import *
from Auth.serializers import BlogProfileSerializer

class CollegeGallerySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CollegeGallery
        fields = '__all__'

class CollegeVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CollegeVideo
        fields = '__all__'


class CourseFeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseFee
        fields = '__all__'


class EligibilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Eligibility
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FAQ
        fields = '__all__'
        
class SimpleCourseFeeSerializer(serializers.ModelSerializer):
    academic_year = SimpleAcademicYearSerializer(read_only=True)
    
    class Meta:
        model = CourseFee
        exclude = ('created_at', 'updated_at',)


class SimpleEligibilitySerializer(serializers.ModelSerializer):
    exam = SimpleExamSerializer(read_only=True)
    
    class Meta:
        model = Eligibility
        exclude = ('created_at', 'updated_at',)
        
class SimpleFAQSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FAQ
        exclude = ('created_at', 'updated_at',)


class BasicCollegeSerializer(serializers.ModelSerializer):
    organization_type = SimpleOrganizationTypeSerializer(read_only=True)
    college_type = SimpleCollegeTypeSerializer(read_only=True)
    course_category = SimpleCourseCategorySerializer(many=True, read_only=True)
    course_subcategory = SimpleCourseSubcategorySerializer(many=True, read_only=True)
    eligibility = SimpleEligibilitySerializer(many=True,read_only=True)
    course_fee = SimpleCourseFeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = College
        fields = ['name', 'logo','views','image', 'rank','rating','established_year', 'organization_type','college_type','course_category','course_subcategory','course_fee','eligibility',
                   'country', 'state', 'city', 'current_address', 'permanent_address','zipcode',
                  'created_at', 'updated_at','slug' ]

class CollegeSerializer(serializers.ModelSerializer):
    organization_type = SimpleOrganizationTypeSerializer(read_only=True)
    college_type = SimpleCollegeTypeSerializer(read_only=True)
    course_category = SimpleCourseCategorySerializer(many=True, read_only=True)
    faq = SimpleFAQSerializer(many=True, read_only=True)
    eligibility = SimpleEligibilitySerializer(many=True,read_only=True)
    course_fee = SimpleCourseFeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = College
        fields = '__all__'


class FullCourseFeeSerializer(serializers.ModelSerializer):
    academic_year = SimpleAcademicYearSerializer(read_only=True)
    course_subcategory = SimpleCourseSubcategorySerializer(read_only=True)
    college = CollegeSerializer(read_only=True)

    class Meta:
        model = CourseFee
        fields = '__all__'
        
class SimpleCollegeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = College
        fields = ('id','name','logo','slug',)

class CollegeApplicationSerializer(serializers.ModelSerializer):
    student = BlogProfileSerializer(read_only=True)
    college = SimpleCollegeSerializer(read_only=True)
    course_category = OnlyCourseCategorySerializer( read_only=True)
    course_subcategory = OnlyCourseSubcategorySerializer(read_only=True)
    course_stream = OnlyCourseStreamSerializer(read_only=True)
    
    class Meta:
        model = CollegeApplication
        fields = '__all__'

class CollegeLeadsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CollegeApplication
        fields = '__all__'


# Menu
class CategoryCollegeSerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    colleges= SimpleCollegeSerializer(many=True,read_only=True)
    exams= SimpleExamSerializer(many=True,read_only=True)

    class Meta:
        model = College
        fields = ('id','course_category','colleges','exams','slug')
        
        
        

class CollegeNewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CollegeNews
        fields = '__all__'

class ListCollegeNewsSerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    user = BlogProfileSerializer(read_only=True)

    class Meta:
        model = CollegeNews
        fields = ('id','slug','user','college','title','image','post','views','course_category','created_at','updated_at',)


class SingleCollegeNewsSerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    user = BlogProfileSerializer(read_only=True)

    class Meta:
        model = CollegeNews
        fields = '__all__'

# Notify
class NotifyCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('id', 'slug', 'name', 'logo', 'rating')



# Only
class OnlyCollegeSerializer(serializers.ModelSerializer):
    course_subcategory = serializers.PrimaryKeyRelatedField(queryset=CourseSubcategory.objects.all(), many=True)
    
    class Meta:
        model = College
        fields = '__all__'

class AllEligibilitySerializer(serializers.ModelSerializer):
    # course_category = OnlyCourseCategorySerializer()
    # course_subcategory = OnlyCourseSubcategorySerializer()
    # course_stream = OnlyCourseStreamSerializer()
    # college = SimpleCollegeSerializer()
    # exam = SimpleExamSerializer()
    class Meta:
        model = Eligibility
        fields = '__all__'
        
        
class AllCourseFeeSerializer(serializers.ModelSerializer):
    # academic_year = SimpleAcademicYearSerializer(read_only=True)
    # course_subcategory = SimpleCourseSubcategorySerializer()
    # college = SimpleCollegeSerializer(read_only=True)
    # course_stream = OnlyCourseStreamSerializer(read_only=True)
    class Meta:
        model = CourseFee
        fields = '__all__'

# class CourseFeeSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CourseFee
#         fields = '__all__'


# class CollegeSerializer(serializers.ModelSerializer):
#     course_category = SimpleCourseCategorySerializer(many=True, read_only=True)
#     course_subcategory = SimpleCourseSubcategorySerializer(many=True, read_only=True)
#     course_stream = CourseStreamSerializer(many=True, read_only=True)
#     course_fee = SingleCourseFeeSerializer(many=True, read_only=True)
#     eligibility = SingleEligibilitySerializer(many=True, read_only=True)
#
#     class Meta:
#         model = College
#         fields = ['name', 'logo', 'type', 'established_year', 'category', 'course_category', 'course_subcategory',
#                   'course_stream', 'course_fee', 'eligibility', 'country', 'state', 'city', 'address', 'zipcode',
#                   'created_at', 'updated_at', ]
#         # 'fields = '__all__''

# Dashboard Update