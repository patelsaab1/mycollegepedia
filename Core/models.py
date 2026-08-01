from django.db import models
from Main.models import TimeStamp,SEO
from ckeditor.fields import RichTextField
from Auth.myvalidator import numeric,mobile_validator
from imagekit.models import ProcessedImageField
from Auth.models import User

# Create your models here.
class SiteConfig(SEO,TimeStamp, models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    favicon = models.ImageField(verbose_name='favicon', upload_to='siteconfig')
    logo = ProcessedImageField(
        upload_to='siteconfig',
        format='WEBP', 
        options={'quality': 70},verbose_name="logo"
    )
    primary_mobile = models.CharField(verbose_name="primary mobile number", max_length=13,
                                      validators=[mobile_validator],
                                      help_text="Alphabets and special characters are not allowed.")
    secondary_mobile = models.CharField(verbose_name="secondary mobile number", max_length=13,
                                        validators=[mobile_validator],
                                        help_text="Alphabets and special characters are not allowed.", blank=True,
                                        null=True)
    email = models.EmailField(verbose_name='email', max_length=255)
    whatsapp = models.URLField(verbose_name='whatsapp url',blank=True,null=True)
    facebook = models.URLField(verbose_name='facebook url',blank=True,null=True)
    instagram = models.URLField(verbose_name='instagram url',blank=True,null=True)
    thread = models.URLField(verbose_name='thread url',blank=True,null=True)
    linkedin = models.URLField(verbose_name='linkedin url',blank=True,null=True)
    twitter = models.URLField(verbose_name='twitter url',blank=True,null=True)
    youtube = models.URLField(verbose_name='youtube url',blank=True,null=True)
    playstore = models.URLField(verbose_name='playstore url',blank=True,null=True)
    appstore = models.URLField(verbose_name='appstore url',blank=True,null=True)
    short_description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Site Config'
        verbose_name_plural = 'Site Config'
        ordering = ["-id"]
    def __str__(self):
        return self.title


class Slider(TimeStamp, models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    image = ProcessedImageField(
        upload_to='core/slider',
        format='WEBP', 
        options={'quality': 90},verbose_name="slider image"
    )
    short_description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Slider'
        ordering = ["-title"]
        
    def __str__(self):
        return self.title


class About(SEO,TimeStamp, models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    description = RichTextField()

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'
        ordering = ["-id"]
        
    def __str__(self):
        return self.title
        
class PrivacyPolicy(SEO,TimeStamp, models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    description = RichTextField()

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policy'
        ordering = ["-id"]
        
    def __str__(self):
        return self.title

class TermsAndCondition(SEO,TimeStamp, models.Model):
    title = models.CharField(verbose_name='title', max_length=200)
    description = RichTextField()

    class Meta:
        verbose_name = 'Terms & Condition'
        verbose_name_plural = 'Terms & Condition'
        ordering = ["-id"]
        
    def __str__(self):
        return self.title

class Contact(TimeStamp, models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(verbose_name="mobile number", max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        ordering = ["-id"]
        
    def __str__(self):
        return f"{self.name} {self.email} {self.subject}"

class Testimonial(TimeStamp, models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    description = models.TextField(verbose_name='Feedback')
    rating = models.PositiveIntegerField(choices=RATING, default=5)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.user} {self.rating}"
        
        
class Feedback(TimeStamp):
    name = models.CharField(max_length=200, verbose_name='full name')
    phone = models.CharField(verbose_name="mobile number", max_length=13,
                             validators=[mobile_validator],
                             help_text="Alphabets and special characters are not allowed.")
    email = models.EmailField(verbose_name='email', max_length=255)
    message = models.TextField(verbose_name='message')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.phone}"
        
        
class Experience(TimeStamp):
    note = models.TextField(verbose_name='note')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'
        ordering = ["-id"]

    def __str__(self):
        return f"{self.rating}"
