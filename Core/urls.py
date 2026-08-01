from django.urls import path
from .views import SiteConfigView,AboutView,SliderListView,ContactCreateView,PrivacyPolicyView,TermsAndConditionView,TestimonialListView,FeedbackCreateView,ExperienceCreateView
urlpatterns = [
    path('site-config/', SiteConfigView.as_view(), name='site-config'),
    path('about/', AboutView.as_view(), name='about'),
    path('slider/', SliderListView.as_view(), name='slider'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('terms/', TermsAndConditionView.as_view(), name='terms'),
    path('testimonial/', TestimonialListView.as_view(), name='testimonial'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('experience/', ExperienceCreateView.as_view(), name='experience'),
]
