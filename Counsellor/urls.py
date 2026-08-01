from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'counsellor-detail', CounsellorViewSet,basename='counsellor-detail')
router.register(r'director-detail', DirectorViewSet,basename='director-detail')
router.register(r'awards-achivements', CounsellorGalleryViewSet,basename='awards-achivement')
router.register(r'intro-video', CounsellorVideoViewSet,basename='intro-video')
router.register(r'counsellor-testimonial', CounsellorTestimonialViewSet,basename='counsellor-testimonial')
router.register(r'counsellor-leads', LeadsViewSet,basename='counsellor-leads')
router.register(r'counsellor', CounsellorViewOnly,basename='counsellor')
router.register(r'faqs', FAQViewSet,basename='faqs')
router.register(r'news', NewsViewSet,basename='news')
urlpatterns = [
    
   path('register/', CounsellorCreateView.as_view(), name='register'),
   path('director-register/', DirectorCreateView.as_view(), name='director-register'),
   path('organization-type/',OrganizationTypeListView.as_view(),name='organization-type'),
   path('testimonial/<int:counsellor_id>/',CounsellorTestimonialListView.as_view(),name='testimonial'),
   path('apply/', CounsellorApplicationCreateView.as_view(), name='apply'),
   path('student-apply/', StudentAppliedCounsellorView.as_view(), name='student-apply'),
   path('faq/', FAQListAPIView.as_view(), name='faq'),
   path('news-articles/<int:college_id>/', NewsListView.as_view(), name='news-articles'),
   path('news-article/<str:slug>/',NewsDetailView.as_view(),name='news-article-detail'),
   path('counsellor-gallery/<int:counsellor_id>/',CounsellorGalleryListView.as_view(),name='counsellor_gallery'),
   path('counsellor-video/<int:counsellor_id>/',CounsellorVideoListView.as_view(),name='counsellor_video'),
    
   
   # Notify
   path('notify-counsellors/', NotifyCounsellorAPIView.as_view(), name='notify-counsellors'),
   path('', include(router.urls)),
]
