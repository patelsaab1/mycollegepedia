from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from General.permissions import IsCounsellor
from .models import *
from .serializers import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# Register
class CounsellorCreateView(CreateAPIView):
    queryset = Counsellor.objects.all()
    serializer_class = CounsellorCreateSerializer
    permission_classes = (AllowAny,)


class DirectorCreateView(CreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (AllowAny,)



# Basic
class OrganizationTypeListView(ListAPIView):
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer
    permission_classes = (AllowAny,)
    
    
class CounsellorViewOnly(viewsets.ModelViewSet):
    queryset = Counsellor.objects.all()
    serializer_class = CounsellorSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get',]
    lookup_field = 'slug'
    
    def get_object(self):
        counsellor = super().get_object()
        counsellor.increase_views()
        return counsellor
        
        
# Counsellor Gallery
class CounsellorGalleryListView(ListAPIView):
    serializer_class = CounsellorGallerySerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        queryset = CounsellorGallery.objects.filter(counsellor_id=counsellor_id)
        return queryset
        

# Counsellor Video
class CounsellorVideoListView(ListAPIView):
    serializer_class = CounsellorVideoSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        queryset = CounsellorVideo.objects.filter(counsellor_id=counsellor_id)
        return queryset        
        


class CounsellorTestimonialListView(ListAPIView):
    queryset = CounsellorTestimonial.objects.all()
    serializer_class = CounsellorTestimonialSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        queryset = CounsellorTestimonial.objects.filter(counsellor_id=counsellor_id)
        return queryset


class CounsellorApplicationCreateView(CreateAPIView):
    queryset = Leads.objects.all()
    serializer_class = LeadsSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        student_email = instance.student.email 
        self.send_update_email(student_email, instance)
        
        
    def send_update_email(self, email, application):
        subject = 'Admission Bazaar | Counsellor Application Received'
        message_html = render_to_string('email_templates/counsellor_application_student_email.html', {
            'name': application.student.name,
            'company_name': application.counsellor.company_name
        })
        sender_email = 'Admission Bazaar <support@mycollegepedia.com>'
        recipient_email = email

        try:
            email = EmailMessage(
                subject,
                message_html,
                sender_email,
                [recipient_email,'mycollegepedia@gmail.com']
            )
            email.content_subtype = 'html' 
            email.send()
        except Exception as e:
            print(f"Failed to send update email to {email}: {str(e)}")



class StudentAppliedCounsellorView(ListAPIView):
    serializer_class = OnlyLeadsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        student = self.request.user.student
        try:
            queryset = Leads.objects.filter(student=student)
            return queryset
        except CounsellorAdmin.DoesNotExist:
            return Leads.objects.none()

class FAQListAPIView(ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        queryset = FAQ.objects.filter(counsellor_id=counsellor_id)
        return queryset
        
# News
class NewsListFilter(filters.FilterSet):
    class Meta:
        model = News
        fields = {'course_category': ['exact']}


class NewsListView(ListAPIView):
    queryset = News.objects.filter(status='PUBLIC')
    serializer_class = ListNewsSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsListFilter
    
    def get_queryset(self):
        counsellor_id = self.kwargs['counsellor_id']
        queryset = News.objects.filter(counsellor_id=counsellor_id)
        return queryset


class NewsDetailView(RetrieveAPIView):
    queryset = News.objects.filter(status='PUBLIC')
    serializer_class = SingleNewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_object(self):
        news = super().get_object()
        news.increase_views()
        return news

# Notify
class NotifyCounsellorAPIView(ListAPIView):
    serializer_class = NotifyCounsellorSerializer

    def get_queryset(self):
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())

        queryset = Counsellor.objects.filter(
            models.Q(created_at__gte=start_of_week) |
            models.Q(updated_at__gte=start_of_week)
        )
        return queryset


# Counsellor Dashboard
class CounsellorViewSet(viewsets.ModelViewSet):
    queryset = Counsellor.objects.all()
    serializer_class = CounsellorSerializer
    permission_classes = [IsAuthenticated, IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch', ]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Counsellor.objects.filter(counsellor_user=user)
        else:
            return Counsellor.objects.none()


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticated, IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Director.objects.filter(counsellor=user.counselloradmin.counsellor)
        else:
            return Director.objects.none()
            
# CounsellorGallery    
class CounsellorGalleryViewSet(viewsets.ModelViewSet):
    queryset = CounsellorGallery.objects.all()
    serializer_class = CounsellorGallerySerializer
    permission_classes = [IsAuthenticated,IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CounsellorGallery.objects.filter(counsellor=user.counselloradmin.counsellor)
        else:
            return CounsellorGallery.objects.none()
   
# CounsellorVideo   
class CounsellorVideoViewSet(viewsets.ModelViewSet):
    queryset = CounsellorVideo.objects.all()
    serializer_class = CounsellorVideoSerializer
    permission_classes = [IsAuthenticated,IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CounsellorVideo.objects.filter(counsellor=user.counselloradmin.counsellor)
        else:
            return CounsellorVideo.objects.none()
                  

class CounsellorTestimonialViewSet(viewsets.ModelViewSet):
    queryset = CounsellorTestimonial.objects.all()
    serializer_class = CounsellorTestimonialSerializer
    permission_classes = [IsAuthenticated, IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CounsellorTestimonial.objects.filter(counsellor=user.counselloradmin.counsellor)
        else:
            return CounsellorTestimonial.objects.none()
    
    
class LeadsViewSet(viewsets.ModelViewSet):
    queryset = Leads.objects.all()
    serializer_class = OnlyLeadsSerializer
    permission_classes = [IsAuthenticated, IsCounsellor]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        counsellor_user = self.request.user.counselloradmin
        if counsellor_user.is_authenticated:
            return Leads.objects.filter(counsellor__counsellor_user=counsellor_user)
        else:
            return Leads.objects.none()
            
    def perform_update(self, serializer):
        instance = serializer.save()
        student_email = instance.student.email 
        self.send_update_email(student_email, instance)

    def send_update_email(self, email, application):
        subject = 'Admission Bazaar | Update on Your Counsellor Application'
        message_html = render_to_string('email_templates/counsellor_application_status.html', {
            'name': application.student.name,
            'company_name': application.counsellor.company_name,
            'status': application.status  # Assuming there is a status field
        })
        sender_email = 'Admission Bazaar <support@mycollegepedia.com>'
        recipient_email = email

        try:
            email = EmailMessage(
                subject,
                message_html,
                sender_email,
                [recipient_email,'mycollegepedia@gmail.com']
            )
            email.content_subtype = 'html'  # Indicating the email content is in HTML format
            email.send()
        except Exception as e:
            print(f"Failed to send update email to {email}: {str(e)}")

            
            
class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated, IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FAQ.objects.filter(counsellor=user.counselloradmin.counsellor)
        else:
            return FAQ.objects.none()
            
# News and article
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated,IsCounsellor]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return News.objects.filter(counsellor=user.counselloradmin.counsellor)
        else:
            return News.objects.none()
