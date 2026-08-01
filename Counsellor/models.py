from django.db import models
from Main.models import TimeStamp, Address, SEO, SocialMedia
from Auth.models import CounsellorAdmin
from General.models import CourseCategory, AcademicYear, CourseSubcategory, CourseStream
from imagekit.models import ProcessedImageField
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from Auth.models import Student
from Auth.myvalidator import *


# Create your models here.
class Counsellor(SocialMedia, TimeStamp, SEO, Address, models.Model):
    counsellor_user = models.OneToOneField(CounsellorAdmin, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, verbose_name='company name')
    area_of_operation = models.ManyToManyField(CourseCategory)
    logo = ProcessedImageField(
        upload_to='counsellor/logo',
        format='WEBP',
        options={'quality': 70}, verbose_name="logo"
    )
    image = ProcessedImageField(
        upload_to='counsellor/image',
        format='WEBP',
        options={'quality': 70}, verbose_name="image"
    )
    company_certificate = models.FileField(upload_to='counsellor/company', verbose_name='company certificate')
    gst = models.CharField(verbose_name='GST Number', max_length=15, blank=True, null=True,
                           validators=[alphanumeric('GST Number'), maximum(15, 'GST Number'),
                                       minimum(15, 'GST Number')],
                           help_text='Special characters are not allowed')
    pan_no = models.CharField(verbose_name='Pan Card Number', max_length=10, blank=True, null=True,
                              validators=[alphanumeric('Pan Card Number'), maximum(10, 'Pan Card Number'),
                                          minimum(10, 'Pan Card Number')],
                              help_text='Special characters are not allowed')
    pan_card = ProcessedImageField(
        upload_to='counsellor/pan',
        format='WEBP',
        options={'quality': 70}, verbose_name="pan card"
    )
    overview = RichTextField(verbose_name='overview')
    success_story = RichTextField(blank=True, null=True)
    registration_date = models.DateField(max_length=8, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    slug = AutoSlugField(populate_from='company_name', unique=True, editable=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name

    def increase_views(self):
        self.views += 1
        self.save()



class OrganizationType(TimeStamp, models.Model):
    title = models.CharField(max_length=20, verbose_name='organization title')

    class Meta:
        verbose_name = 'Organization Type'
        verbose_name_plural = 'Organization Types'

    def __str__(self):
        return self.title


class Director(SocialMedia, TimeStamp, models.Model):
    IDENTITY_CHOICES = (
        ('Aadhar', 'Aadhar Card'),
        ('Pan', 'Pan Card'),
        ('Voter', 'Voter ID'),
        ('Driving', 'Driving License'),
        ('Passport', 'Passport')
    )
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE, verbose_name='organization type')
    name = models.CharField(max_length=100, verbose_name="director name")
    profile = ProcessedImageField(
        upload_to='counsellor/profile',
        format='WEBP',
        options={'quality': 70}, verbose_name="profile"
    )
    identity = models.CharField(max_length=10, choices=IDENTITY_CHOICES, verbose_name="identity",default='Aadhar')
    id_proof = models.FileField(upload_to='counsellor/id_proof')

    class Meta:
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'

    def __str__(self):
        return f"{self.name}"

class CounsellorGallery(TimeStamp, models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = ProcessedImageField(
        upload_to='counsellor/gallery',
        format='WEBP', 
        options={'quality': 70},verbose_name="image"
    )
    alt = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Award & Achivement '
        verbose_name_plural = 'Awards & Achivements '
        ordering = ["title"]
    def __str__(self):
        return self.title
        
class CounsellorVideo(TimeStamp, models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    videourl = models.URLField(verbose_name='video url', blank=True, null=True)
    alt = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Introductory Video'
        verbose_name_plural = 'Introductory Videos'
    def __str__(self):
        return self.title


class CounsellorTestimonial(TimeStamp, models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to='counsellor/testimonial',
        format='WEBP',
        options={'quality': 70}, verbose_name="image",
        blank=True, null=True
    )
    name = models.CharField(max_length=100, verbose_name="name")
    description = models.TextField(verbose_name='Feedback')
    rating = models.PositiveIntegerField(choices=RATING, default=5)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} {self.rating}"
        
        
class Leads(TimeStamp, models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE)
    course_stream = models.ForeignKey(CourseStream, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return f"{self.student} - {self.counsellor} - {self.status}"

class FAQ(TimeStamp, models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, related_name='faq')
    question = models.CharField(verbose_name='questions', max_length=200)
    answer = RichTextField(verbose_name='answer')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ["-counsellor"]

    def __str__(self):
        return f"{self.counsellor.company_name} {self.question}"
        
        
class CounsellorGallery(TimeStamp, models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = ProcessedImageField(
        upload_to='counsellor/gallery',
        format='WEBP', 
        options={'quality': 70},verbose_name="image"
    )
    alt = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Award & Achivement'
        verbose_name_plural = 'Awards & Achivements'
        ordering = ["title"]
    def __str__(self):
        return self.title
        
class CounsellorVideo(TimeStamp, models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    videourl = models.URLField(verbose_name='video url', blank=True, null=True)
    alt = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Introductory Video'
        verbose_name_plural = 'Introductory Videos'
    def __str__(self):
        return self.title
        


class News(SEO, TimeStamp, models.Model):
    STATUS = {
        ('DRAFT', 'DRAFT'),
        ('PUBLIC', 'PUBLIC'),
    }
    user = models.ForeignKey(CounsellorAdmin, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='title')
    image = ProcessedImageField(
        upload_to='counsellor/news',
        format='WEBP', 
        options={'quality': 50},verbose_name="thumbnail"
    )
    post = RichTextField(verbose_name='post')
    status = models.CharField(choices=STATUS, max_length=10)
    slug = AutoSlugField(populate_from='title', unique=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'News & Article'
        verbose_name_plural = 'News & Articles'
        ordering = ["-title"]

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save()