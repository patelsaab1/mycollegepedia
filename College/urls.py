from django.urls import path,include
from rest_framework import routers
from College.views import CollegeListView, CollegeRetrieveView, CollegeGalleryListView, CourseFeeRetrieveView, \
    EligibilityRetrieveView, CourseFeeViewSet, CollegeApplicationCreateView, CollegeApplicationListView, \
    StudentAppliedCollegesView,CollegeAppliedCollegesView,CategoryCollegeView,NewsListView,NewsDetailView,NewsViewSet,CollegeVideoListView,CollegeViewSet,CollegeGalleryViewSet,CollegeVideoViewSet,CourseFeeSet,CollegeAppliedViewSet,EligibilityViewSet,FAQViewSet,CollegeUpdateView,NotifyCollegesAPIView

router = routers.DefaultRouter()
router.register(r'coursefees', CourseFeeViewSet,basename='coursefees')
router.register(r'college-detail', CollegeViewSet,basename='collegeview')
router.register(r'awards-achivements', CollegeGalleryViewSet,basename='awards-achivement')
router.register(r'intro-video', CollegeVideoViewSet,basename='intro-video')
router.register(r'course-fees', CourseFeeSet,basename='course-fees')
router.register(r'college-leads', CollegeAppliedViewSet,basename='college-leads')
router.register(r'college-eligibility', EligibilityViewSet,basename='college-eligibility')
router.register(r'college-faq', FAQViewSet,basename='college-faq')
router.register(r'news', NewsViewSet,basename='news')
# Update
router.register(r'college-update', CollegeUpdateView,basename='college-update')
urlpatterns = [
    path('all-college/',CollegeListView.as_view(),name='all_college'),
    path('college/<str:slug>/',CollegeRetrieveView.as_view(),name='college'),
    path('college-gallery/<int:college_id>/',CollegeGalleryListView.as_view(),name='college_gallery'),
    path('college-video/<int:college_id>/',CollegeVideoListView.as_view(),name='college_video'),
    path('course-fee/<int:pk>/',CourseFeeRetrieveView.as_view(),name='course_fee'),
    # path('course-fee/',CourseFeeViewSet.as_view({'get': 'retrieve'}),name='all_course_fee'),
    path('apply/', CollegeApplicationCreateView.as_view(), name='apply-to-college'),
    path('student-applied-colleges/', StudentAppliedCollegesView.as_view(), name='student-applied-colleges'),
    path('college-applied-colleges/', CollegeAppliedCollegesView.as_view(), name='college-applied-colleges'),
    path('applications/', CollegeApplicationListView.as_view(), name='college-applications'),
    path('eligibility/<int:pk>/',EligibilityRetrieveView.as_view(),name='eligibility'),
    path('category-colleges/', CategoryCollegeView.as_view(), name='category_colleges'),
    path('news-articles/<int:college_id>/', NewsListView.as_view(), name='news-articles'),
    path('news-article/<str:slug>/',NewsDetailView.as_view(),name='news-article-detail'),
    # Notify
    path('notify-colleges/', NotifyCollegesAPIView.as_view(), name='notify-colleges'),

    path('', include(router.urls)),
]
