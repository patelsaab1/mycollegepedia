from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Main.views import welcome_redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('',welcome_redirect,name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('account/',include('Auth.urls')),
    path('general-setting/', include('General.urls')),
    path('college/', include('College.urls')),
    path('counsellor/', include('Counsellor.urls')),
    path('main/',include('Main.urls')),
    path('site/',include('Core.urls')),
    path('blog/',include('Blog.urls')),
    path('exam/',include('Exam.urls')),

    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Spectacular url
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)