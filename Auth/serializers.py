from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Auth.models import Student, Education, User,CollegeAdmin,CounsellorAdmin
from Main.models import Religion, Category


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    password = serializers.CharField()
    confirmPassword = serializers.CharField()



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'name', 'mobile', 'password']


class CounsellorRegisterSerializer(serializers.ModelSerializer):
    religion = serializers.PrimaryKeyRelatedField(queryset=Religion.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = CounsellorAdmin
        fields = ['email', 'name', 'mobile', 'profile', 'gender', 'dob', 'religion', 'category', 'brand_name', 'password']
        extra_kwargs = {'profile': {'required': True}, 'gender': {'required': True}, 'dob': {'required': True},
                        'religion': {'required': True}, 'category': {'required': True},
                        'brand_name': {'required': True},
                       }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CounsellorAdmin(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.is_counsellor = True
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_staff', 'is_superuser', 'is_active','is_student','is_counsellor','is_college')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile', 'profile', 'gender', 'dob', 'religion',
                  'category', 'country', 'state', 'city', 'current_address','permanent_address' ,'zipcode','is_active','is_staff','is_student','is_counsellor','is_superuser']

class BlogProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'profile', 'gender',]


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'mobile', 'profile', 'gender', 'dob', 'religion','category',
                  'course_interest', 'country', 'state', 'city', 'current_address','permanent_address', 'zipcode',]

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        
        
class CollegeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeAdmin
        fields = ['id', 'name', 'email', 'mobile', 'profile', 'gender', 'dob', 'religion','category',
                  'department','designation', 'country', 'state', 'city', 'current_address','permanent_address', 'zipcode',]
                  
                  
class CounsellorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounsellorAdmin
        fields = ['id', 'name', 'email', 'mobile', 'profile', 'gender', 'dob', 'religion','category', 'brand_name',]
                  
                  
class StudentSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True,read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'mobile', 'profile', 'gender', 'dob', 'religion','category',
                  'course_interest', 'country', 'state', 'city', 'current_address','permanent_address', 'zipcode','educations']
