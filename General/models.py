from django.db import models
from django.utils.translation import gettext_lazy as _
from Main.models import TimeStamp
from imagekit.models import ProcessedImageField


# Create your models here.
class AcademicYear(TimeStamp, models.Model):
    year = models.CharField(_('year'), max_length=10, unique=True)
    status = models.BooleanField(_("status"), default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['status'], condition=models.Q(status=True),
                                    name='Only one academic session should be active at a time.')
        ]
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'

    def __str__(self):
        return self.year


class OrganizationType(TimeStamp, models.Model):
    name = models.CharField(_('Organization name'), max_length=100)

    class Meta:
        verbose_name = 'Organization Type'
        verbose_name_plural = 'Organization Types'
        ordering = ["name"]
    def __str__(self):
        return self.name


class CollegeType(TimeStamp, models.Model):
    name = models.CharField(_("name"), max_length=100)

    class Meta:
        verbose_name = 'College Type'
        verbose_name_plural = 'College Types'
        ordering = ["name"]
    def __str__(self):
        return self.name


class CourseType(TimeStamp, models.Model):
    name = models.CharField(_('name'), max_length=100)

    class Meta:
        verbose_name = 'Course Type'
        verbose_name_plural = 'Course Types'
        ordering = ["name"]
        
    def __str__(self):
        return self.name


class CourseCategory(TimeStamp, models.Model):
    image = ProcessedImageField(
        upload_to='course_category/',
        format='WEBP', 
        options={'quality': 70},verbose_name="course category image",null=True,
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'
        ordering = ["name"]
        
    def __str__(self):
        return self.name


class CourseSubcategory(TimeStamp, models.Model):
    exam_type = (
        ('1', 'Semester-wise'),
        ('2', 'Yearly-wise')
    )
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='course_subcategory')
    type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    course_name = models.CharField(_('course subcategory name'), max_length=150)
    exam_type = models.CharField(choices=exam_type, max_length=20)
    duration = models.PositiveIntegerField(_('course subcategory duration (In Year)'))
    semester = models.PositiveIntegerField(_('semester'), blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Course Subcategory'
        verbose_name_plural = 'Course Subcategories'
        ordering = ["course_name"]
        
    def save(self, *args, **kwargs):
        if self.exam_type == '1':
            self.semester = self.duration * 2
        else:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name


class CourseStream(TimeStamp, models.Model):
    course_subcategory = models.ForeignKey(CourseSubcategory, on_delete=models.CASCADE, related_name='course_stream')
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Course Stream'
        verbose_name_plural = 'Course Streams'
        ordering = ["name","course_subcategory"]
        
    def __str__(self):
        return f"{self.course_subcategory.course_name} - {self.name}"
