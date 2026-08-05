from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from College.filters import CollegeFilter, CourseFeeFilter
from College.models import College, CollegeGallery, CourseFee, Eligibility, CollegeApplication,CollegeNews,CollegeVideo,FAQ
from College.serializers import CollegeSerializer, CollegeGallerySerializer, CourseFeeSerializer, EligibilitySerializer, \
    FullCourseFeeSerializer, CollegeApplicationSerializer,BasicCollegeSerializer,CategoryCollegeSerializer,CollegeNewsSerializer,SingleCollegeNewsSerializer,ListCollegeNewsSerializer,CollegeVideoSerializer,OnlyCollegeSerializer,FAQSerializer,CollegeLeadsSerializer,AllEligibilitySerializer,AllCourseFeeSerializer,NotifyCollegeSerializer
from django_filters import rest_framework as filters
from General.models import CourseCategory
from Exam.models import Exam
from General.permissions import IsCollege
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db import models

# College Category
class CategoryCollegeView(APIView):
    def get(self, request):
        try:
            course_categories = CourseCategory.objects.all()
            serialized_data = []
            for category in course_categories:
                colleges = College.objects.filter(course_category=category)
                exams = Exam.objects.filter(course_category=category)
                serializer = CategoryCollegeSerializer({'course_category': category, 'colleges': colleges,'exams':exams})
                serialized_data.append(serializer.data)

            return Response(serialized_data)
        except CourseCategory.DoesNotExist:
            return Response({'error': 'No course categories found'}, status=404)
# College
class CollegeListView(ListAPIView):
    queryset = College.objects.all()
    serializer_class = BasicCollegeSerializer
    permission_classes = (AllowAny,)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'organization_type__name',  'college_type__name',
                     'state__name', 'city', 'country__name']
    filterset_class = CollegeFilter

class CollegeRetrieveView(RetrieveAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    
    def get_object(self):
        college = super().get_object()
        college.increase_views()
        return college
    
# College Gallery
class CollegeGalleryListView(ListAPIView):
    serializer_class = CollegeGallerySerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        college_id = self.kwargs['college_id']
        queryset = CollegeGallery.objects.filter(college_id=college_id)
        return queryset
        

# College Video
class CollegeVideoListView(ListAPIView):
    serializer_class = CollegeVideoSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        college_id = self.kwargs['college_id']
        queryset = CollegeVideo.objects.filter(college_id=college_id)
        return queryset

        
# Course Fee
class CourseFeeRetrieveView(RetrieveAPIView):
    queryset = CourseFee.objects.all()
    serializer_class = FullCourseFeeSerializer
    # permission_classes = (IsAuthenticated,)

class CourseFeeViewSet(viewsets.ModelViewSet):
    serializer_class = FullCourseFeeSerializer
    filter_class = CourseFeeFilter

    def get_queryset(self):
        queryset = CourseFee.objects.all()
        min_year_fees = self.request.query_params.get('min_year_fees')
        max_year_fees = self.request.query_params.get('max_year_fees')

        if min_year_fees is not None:
            queryset = queryset.filter(year_fees__gte=min_year_fees)
        if max_year_fees is not None:
            queryset = queryset.filter(year_fees__lte=max_year_fees)

        return queryset
# Leads
class CollegeApplicationCreateView(generics.CreateAPIView):
    queryset = CollegeApplication.objects.all()
    serializer_class = CollegeLeadsSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        student_email = instance.student.email 
        self.send_update_email(student_email, instance)
        
        
    def send_update_email(self, email, application):
        subject = 'Admission Bazaar | College Application Received'
        message_html = render_to_string('email_templates/application_student_email.html', {
            'name': application.student.name,
            'college_name': application.college.name
        })
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = email

        try:
            email = EmailMessage(
                subject,
                message_html,
                sender_email,
                [recipient_email, settings.SUPPORT_CC_EMAIL]
            )
            email.content_subtype = 'html' 
            email.send()
        except Exception as e:
            print(f"Failed to send update email to {email}: {str(e)}")

class CollegeApplicationListView(generics.ListAPIView):
    queryset = CollegeApplication.objects.all()
    serializer_class = CollegeApplicationSerializer
    permission_classes = (IsAuthenticated,)
    
class StudentAppliedCollegesView(generics.ListAPIView):
    serializer_class = CollegeApplicationSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        student = self.request.user.student  
        try:
            queryset = CollegeApplication.objects.filter(student=student)
            return queryset
        except CollegeAdmin.DoesNotExist:
            return CollegeApplication.objects.none()
        
class CollegeAppliedCollegesView(generics.ListAPIView):
    serializer_class = CollegeApplicationSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        college_user = self.request.user.collegeadmin 
        try:
            queryset = CollegeApplication.objects.filter(college__college_user=college_user)
            return queryset
        except CollegeAdmin.DoesNotExist:
            return CollegeApplication.objects.none()
# Eligibility       
class EligibilityRetrieveView(RetrieveAPIView):
    queryset = Eligibility.objects.all()
    serializer_class = EligibilitySerializer
    permission_classes = (IsAuthenticated,)
# News
class NewsListFilter(filters.FilterSet):
    class Meta:
        model = CollegeNews
        fields = {'course_category': ['exact']}

class NewsListView(ListAPIView):
    queryset = CollegeNews.objects.filter(status='PUBLIC')
    serializer_class = ListCollegeNewsSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsListFilter
    
    def get_queryset(self):
        college_id = self.kwargs['college_id']
        queryset = CollegeNews.objects.filter(college_id=college_id)
        return queryset

class NewsDetailView(RetrieveAPIView):
    queryset = CollegeNews.objects.filter(status='PUBLIC')
    serializer_class = SingleCollegeNewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_object(self):
        news = super().get_object()
        news.increase_views()
        return news

# Notify    
class NotifyCollegesAPIView(generics.ListAPIView):
    serializer_class = NotifyCollegeSerializer

    def get_queryset(self):
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())

        queryset = College.objects.filter(
            models.Q(created_at__gte=start_of_week) |
            models.Q(updated_at__gte=start_of_week)
        )
        return queryset
    
# College Dashboard
class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch',]
    lookup_field = 'slug'
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return College.objects.filter(college_user=user)
        else:
            return College.objects.none()
    
# ColllegeGallery    
class CollegeGalleryViewSet(viewsets.ModelViewSet):
    queryset = CollegeGallery.objects.all()
    serializer_class = CollegeGallerySerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CollegeGallery.objects.filter(college=user.collegeadmin.college)
        else:
            return CollegeGallery.objects.none()
   
# CollegeVideo   
class CollegeVideoViewSet(viewsets.ModelViewSet):
    queryset = CollegeVideo.objects.all()
    serializer_class = CollegeVideoSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CollegeVideo.objects.filter(college=user.collegeadmin.college)
        else:
            return CollegeVideo.objects.none()
            
# CourseFee
class CourseFeeSet(viewsets.ModelViewSet):
    queryset = CourseFee.objects.all()
    serializer_class = AllCourseFeeSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CourseFee.objects.filter(college=user.collegeadmin.college)
        else:
            return CourseFee.objects.none()
          
# CollegeApplied            
class CollegeAppliedViewSet(viewsets.ModelViewSet):
    queryset = CollegeApplication.objects.all()
    serializer_class = CollegeApplicationSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'put', 'patch']
    def get_queryset(self):
        college_user = self.request.user.collegeadmin
        if college_user.is_authenticated:
            return CollegeApplication.objects.filter(college__college_user=college_user)
        else:
            return CollegeApplication.objects.none()
            
    def perform_update(self, serializer):
        instance = serializer.save()
        student_email = instance.student.email 
        self.send_update_email(student_email, instance)

    def send_update_email(self, email, application):
        subject = 'Admission Bazaar | Update on Your College Application'
        message_html = render_to_string('email_templates/application_status.html', {
            'name': application.student.name,
            'college_name': application.college.name,
            'status': application.status  # Assuming there is a status field
        })
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = email

        try:
            email = EmailMessage(
                subject,
                message_html,
                sender_email,
                [recipient_email, settings.SUPPORT_CC_EMAIL]
            )
            email.content_subtype = 'html'  # Indicating the email content is in HTML format
            email.send()
        except Exception as e:
            print(f"Failed to send update email to {email}: {str(e)}")

    
    
    # def get_queryset(self):
    #     college_user = self.request.user.collegeadmin 
    #     try:
    #         queryset = CollegeApplication.objects.filter(college__college_user=college_user)
    #         return queryset
    #     except CollegeAdmin.DoesNotExist:
    #         return CollegeApplication.objects.none()
    
# Eligibility
class EligibilityViewSet(viewsets.ModelViewSet):
    queryset = Eligibility.objects.all()
    serializer_class = AllEligibilitySerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Eligibility.objects.filter(college=user.collegeadmin.college)
        else:
            return Eligibility.objects.none()
            
# FAQs
class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FAQ.objects.filter(college=user.collegeadmin.college)
        else:
            return FAQ.objects.none()            
            
# Update Api
class CollegeUpdateView(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = OnlyCollegeSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch',]
    lookup_field = 'slug'
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return College.objects.filter(college_user=user)
        else:
            return College.objects.none()
            
# News and article
class NewsViewSet(viewsets.ModelViewSet):
    queryset = CollegeNews.objects.all()
    serializer_class = CollegeNewsSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CollegeNews.objects.filter(college=user.collegeadmin.college)
        else:
            return CollegeNews.objects.none()
