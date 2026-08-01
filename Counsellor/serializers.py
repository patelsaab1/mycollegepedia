from rest_framework import serializers
from General.serializers import OnlyCourseCategorySerializer, OnlyCourseStreamSerializer, \
    OnlyCourseSubcategorySerializer, SimpleCourseCategorySerializer
from Auth.serializers import StudentProfileSerializer
from .models import *
from Auth.serializers import BlogProfileSerializer


class CounsellorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsellor
        exclude = ('meta_title', 'meta_keyword', 'meta_description', 'whatsapp', 'facebook', 'instagram', 'linkedin', 'twitter', 'youtube', 'telegram','success_story', 'views', 'slug',)



class CounsellorGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CounsellorGallery
        fields = '__all__'


class CounsellorVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounsellorVideo
        fields = '__all__'




class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        exclude = ('created_at', 'updated_at',)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class CounsellorTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounsellorTestimonial
        fields = '__all__'


class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'
        
        
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class OnlyCounsellorSerializer(serializers.ModelSerializer):
    area_of_operation = SimpleCourseCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Counsellor
        fields = '__all__'


class OnlyDirectorSerializer(serializers.ModelSerializer):
    counsellor = SimpleCourseCategorySerializer(many=True, read_only=True)
    organization_type = OrganizationTypeSerializer(read_only=True)

    class Meta:
        model = Director
        fields = '__all__'


class OnlyCounsellorTestimonialSerializer(serializers.ModelSerializer):
    counsellor = SimpleCourseCategorySerializer(many=True, read_only=True)

    class Meta:
        model = CounsellorTestimonial
        fields = '__all__'


class OnlyLeadsSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    course_category = OnlyCourseCategorySerializer(read_only=True)
    course_subcategory = OnlyCourseSubcategorySerializer(read_only=True)
    course_stream = OnlyCourseStreamSerializer(read_only=True)

    class Meta:
        model = Leads
        fields = '__all__'
        
        
class CounsellorSerializer(serializers.ModelSerializer):
    area_of_operation = SimpleCourseCategorySerializer(many=True, read_only=True)
    faq = FAQSerializer(many=True,read_only=True)
    class Meta:
        model = Counsellor
        fields = '__all__'
        
# Notify
class NotifyCounsellorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsellor
        fields = ('id', 'slug', 'company_name', 'logo',)

# News
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class ListNewsSerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    user = BlogProfileSerializer(read_only=True)

    class Meta:
        model = News
        fields = ('id','slug','user','counsellor','title','image','post','views','course_category','created_at','updated_at',)


class SingleNewsSerializer(serializers.ModelSerializer):
    course_category = SimpleCourseCategorySerializer(read_only=True)
    user = BlogProfileSerializer(read_only=True)

    class Meta:
        model = News
        fields = '__all__'
