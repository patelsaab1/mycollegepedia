from ckeditor.fields import RichTextField
from django.db import models
from Main.models import TimeStamp,SEO
from General.models import CourseCategory
from autoslug import AutoSlugField
from imagekit.models import ProcessedImageField

# Create your models here.
class Exam(SEO,TimeStamp, models.Model):
    title = models.CharField(max_length=255, verbose_name='exam title')
    description = RichTextField(verbose_name='exam description', blank=True, null=True)
    full_form = models.CharField(max_length=200, verbose_name='full form', blank=True, null=True)
    image = ProcessedImageField(
        upload_to='exam',
        format='WEBP', 
        options={'quality': 70},verbose_name="image",blank=True,null=True,
    )
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,blank=True,null=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True,blank=True, null=True)


    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        ordering = ["-course_category"]

    def __str__(self):
        return self.title


class UpcomingExam(SEO,TimeStamp, models.Model):
    MODE = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='upcoming exam title')
    exam_mode = models.CharField(max_length=20, verbose_name='exam mode', choices=MODE, default='Online')
    description = RichTextField(verbose_name='exam description', blank=True, null=True)
    exam_start_date = models.DateField(verbose_name='exam start date', blank=True, null=True)
    exam_end_date = models.DateField(verbose_name='exam end date', blank=True, null=True)
    application_start_date = models.DateField(verbose_name='application form start date', blank=True, null=True)
    application_end_date = models.DateField(verbose_name='application form end date', blank=True, null=True)
    result = models.DateField(verbose_name='result date', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True,blank=True, null=True)

    class Meta:
        verbose_name = 'Upcoming Exam'
        verbose_name_plural = 'Upcoming Exams'
        ordering = ["-exam"]

    def __str__(self):
        return self.exam.title
