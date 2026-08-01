import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import MyUserManager
from .myvalidator import *
from Main.models import Address,Religion,Category
from General.models import CourseSubcategory
from imagekit.models import ProcessedImageField

class User(AbstractUser, Address):
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('OTHERS', 'OTHERS'),
    )
    username = None
    first_name = None
    last_name = None
    name = models.CharField(_('full name'), max_length=200)
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=True,
        help_text=_("required. email number must be entered in the format: 'example@example.com'."),
        validators=[validate_email],
        error_messages={'unique': _("user with email already exists.")}, )
    profile = ProcessedImageField(
        upload_to='profile',
        format='WEBP', 
        options={'quality': 70}, blank=True,null=True,verbose_name="profile picture"
    )
    gender = models.CharField(_("gender"), choices=GENDER, null=True,max_length=10)
    dob = models.DateField(_("date of birth"), max_length=8, null=True,blank=True)
    mobile = models.CharField(_("mobile number"), max_length=15,
                              help_text="Alphabets and special characters are not allowed.", unique=True)
    religion = models.ForeignKey(Religion,on_delete=models.CASCADE,verbose_name="religion",blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="category",blank=True,null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the staff can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_student = models.BooleanField(
        _("student status"),
        default=False
    )
    is_college = models.BooleanField(
        _("college status"),
        default=False,
    )
    is_counsellor = models.BooleanField(
        _("counsellor status"),
        default=False,
    )
    objects = MyUserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'mobile']

    class Meta:
        verbose_name = _("All User")
        verbose_name_plural = _("All Users")
        swappable = "AUTH_USER_MODEL"
        ordering = ["-id"]

    def __str__(self):
        return f'{self.name} {self.email}'

class Student(User):
    course_interest = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE, null=True,blank=True)
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ["-id"]

    def __str__(self):
        return f'{self.name} {self.email}'

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class PasswordResetToken(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_token')
    validity = models.DateTimeField()

    def __str__(self):
        return self.user.email


class CollegeAdmin(User):
    department = models.CharField(max_length=20, verbose_name="Department")
    designation = models.CharField(max_length=20, verbose_name="Designation", )
    
    class Meta:
        verbose_name = 'College User'
        verbose_name_plural = 'College Users'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.email}"


class Education(models.Model):
    GRADE_SYSTEM = (
        ('CGPA', 'CGPA'),
        ('PERCENTAGE', 'PERCENTAGE'),
    )
    user = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='educations')
    institute = models.CharField(max_length=100, verbose_name='School/College/University')
    institute_name = models.CharField(max_length=200,verbose_name='institute name')
    degree = models.CharField(max_length=100, verbose_name='Degree')
    grade_system = models.CharField(max_length=20, choices=GRADE_SYSTEM, default='CGPA')
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, message="Score cannot be negative"),
            MaxValueValidator(100.00, message="Score cannot be greater than 100"),
        ],
        help_text="Enter a score between 0.00 and 100.00", blank=True, null=True
    )
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.CharField(max_length=50,blank=True, null=True)
    end_date = models.CharField(max_length=50,blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'

    def __str__(self):
        return f'{self.user.email} {self.institute}'
        
        
# class CounsellorAdmin(User):
#     brand_name = models.CharField(verbose_name='brand name', max_length=255)
#     company_certificate = models.FileField(upload_to='counsellor/company', verbose_name='company certificate')
#     gst = models.CharField(verbose_name='GST Number', max_length=15, blank=True, null=True,
#                           validators=[alphanumeric('GST Number'), maximum(15, 'GST Number'),
#                                       minimum(15, 'GST Number')],
#                           help_text='Special characters are not allowed')
#     pan_no = models.CharField(verbose_name='Pan Card Number', max_length=10, blank=True, null=True,
#                               validators=[alphanumeric('Pan Card Number'), maximum(10, 'Pan Card Number'),
#                                           minimum(10, 'Pan Card Number')],
#                               help_text='Special characters are not allowed')
#     pan_card = ProcessedImageField(
#         upload_to='counsellor/pan',
#         format='WEBP',
#         options={'quality': 70},  verbose_name="pan card"
#     )


#     class Meta:
#         verbose_name = 'Company User'
#         verbose_name_plural = 'Company Users'
#         # ordering = ["-id"]

#     def __str__(self):
#         return f"{self.name} {self.email}"

class CounsellorAdmin(User):
    current_address = None
    permanent_address = None
    country = None
    state = None
    city = None
    zipcode = None
    brand_name = models.CharField(verbose_name='brand name', max_length=255)

    class Meta:
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'
        # ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.email}"

