import os
from datetime import timedelta
from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'corsheaders',
    'ckeditor',
    'import_export',
    'Core',
    'Main',
    'Auth',
    'General',
    'College',
    'Exam',
    'Blog',
    'Counsellor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'App.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'App.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.mysql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static

# STATIC_URL = '/static/'
# STATIC_ROOT = '/home/x7nvgmfv66ip/public_html/portal.mycollegepedia.com/static/'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = '/home/x7nvgmfv66ip/public_html/portal.mycollegepedia.com/media/'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
AUTH_USER_MODEL = 'Auth.User'

# TWILIO
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')


CORS_ALLOW_ALL_ORIGINS=True

# Cors Header
CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "http://127.0.0.1:8000",
    "https://localhost:8000",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "https://mycollegepedia.com",
    "https://www.mycollegepedia.com",
    "https://portal.mycollegepedia.com",
]


REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

# JWT 
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# SPECTACULAR

SPECTACULAR_SETTINGS = {
    'TITLE': 'Admission Bazaar API',
    'DESCRIPTION': 'Admission Bazaar is a modern admission platform helping students discover colleges, explore courses, and achieve their academic goals.',
    'VERSION': '7.1.2.3 Beta',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}




# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

SUPPORT_EMAIL = config('SUPPORT_EMAIL', default='Admissionsbazaar@gmail.com')
SUPPORT_PHONE = config('SUPPORT_PHONE', default='9479469454')
DEFAULT_FROM_EMAIL = f'Admission Bazaar <{SUPPORT_EMAIL}>'
SUPPORT_CC_EMAIL = config('SUPPORT_CC_EMAIL', default=SUPPORT_EMAIL)

TEMPLATES_BASE_URL = config('TEMPLATES_BASE_URL')

# UI
JAZZMIN_SETTINGS = {
    "site_title": "Admission Bazaar — Dream • Discover • Succeed",
    "site_header": "Admission Bazaar",
    "site_brand": "Admission Bazaar",
    "site_logo": "assets/img/admission-bazaar-logo.png",
    "login_logo": "assets/img/admission-bazaar-logo.png",
    "login_logo_dark": None,
    "site_logo_classes": None,

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "frontend/assets/img/favicon.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to Admission Bazaar",

    # Copyright on the footer
    "copyright": "Admission Bazaar",
    "version": "7.1.2.3 Beta",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "#", "new_window": True},

        {"name": "Visit Site", "url": "https://mycollegepedia.com/", "new_window": True},

    ],

    "usermenu_links": [
        {"model": "auth.user"}
    ],

    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["Auth", "Core", "Main", "General", "College", "Exam", "Blog","Counsellor", "Core.SiteConfig","Core.Slider","Core.About","Core.Contact","Core.PrivacyPolicy","Core.TermsAndCondition","Core.Testimonial",
                              "Core.Feedback", "Core.Experience",
                              "Main.Religion", "Main.Category", "Main.Country",
                              "Main.State", "General.AcademicYear", "General.OrganizationType",
                              "General.CollegeType", "General.CourseType", "General.CourseCategory",
                              "General.CourseSubCategory", "General.CourseStream", "College.College",
                              "College.CollegeGallery", "College.CollegeVideo","College.CourseFee","College.CollegeApplication","College.Eligibility","College.FAQ","College.CollegeNews","Exam.Exam","Exam.UpcomingExam","Blog.Blog","Counsellor.OrganizationType","Counsellor.Counsellor","Counsellor.Director","Counsellor.Leads","Counsellor.CounsellorTestimonial","Counsellor.News"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-users",
        "auth.CollegeAdmin": "fas fa-user-secret",
        "auth.Student": "fas fa-user-graduate",
        "auth.CounsellorAdmin": "fas fa-user-tie",
        "auth.Group": "fas fa-users-cog",
        # College
        "College.College": "fas fa-university",
        "College.CollegeGallery": "far fa-images",
        "College.CollegeVideo": "fas fa-film",
        "College.CourseFee": "fas fa-money-check-alt",
        "College.Eligibility": "far fa-star",
        "College.CollegeApplication": "fas fa-file-alt",
        "College.FAQ": "fas fa-question",
        "College.CollegeNews": "far fa-newspaper",
        # General
        "General.AcademicYear": "far fa-calendar-alt",
        "General.OrganizationType": "fas fa-school",
        "General.CollegeType": "fas fa-landmark",
        "General.CourseType": "fas fa-book-reader",
        "General.CourseCategory": "fas fa-shapes",
        "General.CourseSubCategory": "fas fa-layer-group",
        "General.CourseStream": "fas fa-sitemap",
        # Main
        "Main.Country": "fas fa-globe-africa",
        "Main.State": "fas fa-flag",
        "Main.Religion": "fas fa-om",
        "Main.Category": "fas fa-atom",
        # Core
        "Core.SiteConfig": "fas fa-globe",
        "Core.Contact": "far fa-comments",
        "Core.About": "far fa-address-card",
        "Core.Slider": "fas fa-images",
        "Core.PrivacyPolicy": "fas fa-user-lock",
        "Core.Testimonial": "far fa-comment-dots",
        "Core.TermsAndCondition": "fas fa-check",
        "Core.Feedback": "fas fa-star",
        "Core.Experience":"far fa-smile",
        # Exam
        "Exam.Exam": "far fa-file-alt",
        "Exam.UpcomingExam": "fas fa-newspaper",
        # Blog
        "Blog.Blog":"fas fa-user-edit",
        "Blog.Tag":"fas fa-tag",
        # Counsellor
        "Counsellor.OrganizationType": "fas fa-sitemap",
        "Counsellor.Counsellor": "fas fa-building",
        "Counsellor.Director": "fas fa-user-friends",
        "Counsellor.CounsellorTestimonial": "far fa-comment-dots",
        "Counsellor.Leads": "fas fa-tasks",
        "Counsellor.FAQ": "fas fa-question",
        "Counsellor.News": "far fa-newspaper",
        
        
       
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-caret-right",
    "default_icon_children": "fas fa-caret-right",
    "related_modal_active": False,

    "custom_css": "assets/myadmin.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    "changeform_format": "horizontal_tabs",
    "language_chooser": None,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-info",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-info",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": False,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS')

# CKEDITOR
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker",'Font', 'FontSize',],
                ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
                 'JustifyRight', 'JustifyBlock'],
                ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"], ['Undo', 'Redo'], ["Source"],['TextColor', 'BGColor'],
                ["Maximize"]],
    }
}

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

CKEDITOR_UPLOAD_PATH = 'content/ckeditor/'

# SESSIONS
# SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1800  # 1/2 hour in seconds
SESSION_SAVE_EVERY_REQUEST = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Lax'

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
