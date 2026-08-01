from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .models import SiteConfig, About, Slider, Contact,PrivacyPolicy,TermsAndCondition,Testimonial,Feedback,Experience
from .serializers import SiteConfigSerializer, AboutSerializer, SliderSerializer, ContactSerializer,PrivacyPolicySerializer,TermsAndConditionSerializer,TestimonialSerializer,FeedbackSerializer,ExperienceSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny



# Create your views here.
class SiteConfigView(generics.RetrieveAPIView):
    serializer_class = SiteConfigSerializer

    def get_object(self):
        try:
            return SiteConfig.objects.latest('created_at')
        except SiteConfig.DoesNotExist:
            raise Http404("No SiteConfig found")

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)



class AboutView(generics.RetrieveAPIView):
    serializer_class = AboutSerializer

    def get_object(self):
        try:
            return About.objects.latest('created_at')
        except About.DoesNotExist:
            raise Http404("No About us found")

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
            
class PrivacyPolicyView(generics.RetrieveAPIView):
    serializer_class = PrivacyPolicySerializer

    def get_object(self):
        try:
            return PrivacyPolicy.objects.latest('created_at')
        except PrivacyPolicy.DoesNotExist:
            raise Http404("No PrivacyPolicy found")

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

class TermsAndConditionView(generics.RetrieveAPIView):
    serializer_class = TermsAndConditionSerializer

    def get_object(self):
        try:
            return TermsAndCondition.objects.latest('created_at')
        except TermsAndCondition.DoesNotExist:
            raise Http404("No Terms & Condition found")

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


class SliderListView(generics.ListAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        subject = 'Admission Bazaar | Thank You for Contacting Us'
        message_html = render_to_string('email/thankyou.html', {'name': instance.name,'subject':instance.subject,'message':instance.message})

        sender_email = 'Admission Bazaar <support@mycollegepedia.com>'
        recipient_email = instance.email

        try:
            email = EmailMessage(
                subject,
                message_html,
                sender_email,
                [recipient_email,'mycollegepedia@gmail.com'],
            )
            email.content_subtype = 'html'
            email.send()

            data = {'message': 'Thank you for contacting us! We will get back to you soon.'}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Email sending error: {e}")
            error_data = {'error': 'An error occurred while sending the email.'}
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

class ExperienceCreateView(generics.CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (AllowAny,)
