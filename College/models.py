from django.db import models
from django.utils.translation import gettext_lazy as _
from Auth.models import CollegeAdmin, Student,User
from General.models import CourseCategory, AcademicYear, CourseSubcategory, OrganizationType, CollegeType, CourseStream
from Main.models import TimeStamp, Address, SEO,SocialMedia
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from Exam.models import Exam
from Main.models import Category
from imagekit.models import ProcessedImageField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class College(SocialMedia,TimeStamp, SEO, Address, models.Model):
    college_user = models.OneToOneField(CollegeAdmin, on_delete=models.CASCADE)
    name = models.CharField(_('College name'), max_length=255,)
    affiliation = models.CharField(max_length=100, verbose_name='Affilation/Affilated College', blank=True, null=True)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE)
    college_type = models.ForeignKey(CollegeType, on_delete=models.CASCADE)
    course_category = models.ManyToManyField(CourseCategory)
    course_subcategory = models.ManyToManyField(CourseSubcategory,blank=True)
    rank = models.PositiveIntegerField(verbose_name='college rank',unique=True,)
    rating = models.DecimalField(verbose_name='rating', blank=True, null=True,
                                 validators=[MinValueValidator(1), MaxValueValidator(5)], max_digits=3,
                                 decimal_places=1, help_text='Enter a rating between 0.0 and 5.0')
    logo = ProcessedImageField(
        upload_to='college/logo',
        format='WEBP', 
        options={'quality': 70},verbose_name="logo"
    )
    image = ProcessedImageField(
        upload_to='college/image',
        format='WEBP', 
        options={'quality': 70},verbose_name="college image"
    )
    established_year = models.IntegerField(_('established year'))
    overview = RichTextField(verbose_name='overview')
    admission_process = RichTextField(verbose_name='admission process',blank=True,null=True)
    specialization = RichTextField(verbose_name='Specialization',blank=True,null=True)
    career_opportunity = RichTextField(verbose_name='Career & Opportunity',blank=True,null=True)
    placement = RichTextField(verbose_name='placement', blank=True, null=True)
    scholarship = RichTextField(verbose_name='Scholarship', blank=True, null=True)
    scope = RichTextField(verbose_name='Scope',blank=True,null=True)
    views = models.PositiveIntegerField(default=0)
    slug = AutoSlugField(populate_from='name', unique=True, editable=True, blank=True, null=True)

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
        ordering = ["name","organization_type","college_type"]
        
    def __str__(self):
        return self.name
        
    def increase_views(self):
        self.views += 1
        self.save()


class CollegeGallery(TimeStamp, models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = ProcessedImageField(
        upload_to='college/gallery',
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
        
class CollegeVideo(TimeStamp, models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    videourl = models.URLField(verbose_name='video url', blank=True, null=True)
    alt = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Introductory Video'
        verbose_name_plural = 'Introductory Videos'
    def __str__(self):
        return self.title


class CourseFee(TimeStamp, models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, limit_choices_to={'status': True})
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='course_fee')
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, blank=True, null=True) #remove blank,null
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE)
    course_stream = models.ForeignKey(CourseStream, on_delete=models.CASCADE,blank=True,null=True)
    year_fees = models.DecimalField(_('year fees'), max_digits=10, decimal_places=2)
    total_fees = models.DecimalField(_('total fees'), max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Course Fee'
        verbose_name_plural = 'Course Fees'
        ordering = ["college","year_fees",]

    def save(self, *args, **kwargs):
        if self.course_subcategory.duration:
            self.total_fees = self.year_fees * self.course_subcategory.duration
        else:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course_subcategory.course_name} {self.year_fees}'


class CollegeApplication(TimeStamp, models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE)
    course_stream = models.ForeignKey(CourseStream, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        verbose_name = 'College Application'
        verbose_name_plural = 'College Applications'
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.student} - {self.college} - {self.status}"


class Eligibility(TimeStamp, models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='eligibility', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE, blank=True, null=True)
    course_stream = models.ForeignKey(CourseStream, on_delete=models.CASCADE, blank=True, null=True)
    eligibility = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField(_('description'), blank=True, null=True)
    application_start_date = models.DateField(_("application start date"), max_length=8, blank=True,null=True)
    application_end_date = models.DateField(_("application end date"), max_length=8, blank=True,null=True)

    class Meta:
        verbose_name = 'Eligibility'
        verbose_name_plural = 'Eligibility'
        ordering = ["-college"]

    def __str__(self):
        return self.eligibility
        
class FAQ(TimeStamp, models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,related_name='faq')
    question = models.CharField(verbose_name='questions', max_length=200)
    answer = RichTextField(verbose_name='answer')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ["-college"]

    def __str__(self):
        return f"{self.college.name} {self.question}"
        
        
        
class CollegeNews(SEO, TimeStamp, models.Model):
    STATUS = {
        ('DRAFT', 'DRAFT'),
        ('PUBLIC', 'PUBLIC'),
    }
    user = models.ForeignKey(CollegeAdmin, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, blank=True, null=True,)
    title = models.CharField(max_length=255, verbose_name='title')
    image = ProcessedImageField(
        upload_to='college/news',
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

