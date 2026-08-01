from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, VerifyOTPView, ResendOTPView, PasswordResetView, ProfileViewSet, \
    EducationViewSet, CustomLoginView, StudentProfileUpdateView, CollegeProfileUpdateView, CounsellorProfileUpdateView, \
    PasswordResetFormAPIView, PasswordResetConfirmAPIView, StudentViewSet, CounsellorRegisterView, \
    CounsellorVerifyOTPView, CounsellorResendOTPView

router = DefaultRouter()
router.register(r'education', EducationViewSet, basename='education')
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('counsellor-register/', CounsellorRegisterView.as_view(), name='counsellor_register'),
    path('counsellor-verify-otp/', CounsellorVerifyOTPView.as_view(), name='counsellor_verify_otp'),
    path('counsellor-resend-otp/', CounsellorResendOTPView.as_view(), name='counsellor_resend_otp'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_form/<email>/<token>/', PasswordResetFormAPIView.as_view(), name='password_reset_form'),
    path('password_reset_confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    path('user/', ProfileViewSet.as_view(), name="user"),
    path('student/<int:pk>/', StudentViewSet.as_view(), name="student"),
    path('student-profile/', StudentProfileUpdateView.as_view(), name='student-profile'),
    path('college-profile/', CollegeProfileUpdateView.as_view(), name='college-profile'),
    path('counsellor-profile/', CounsellorProfileUpdateView.as_view(), name='counsellor-profile'),
    path('', include(router.urls)),
]
