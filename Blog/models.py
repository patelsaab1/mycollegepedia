from Auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from Main.models import TimeStamp, SEO
from General.models import CourseCategory
from imagekit.models import ProcessedImageField
from django.utils import timezone

# Create your models here.
class Blog(SEO, TimeStamp, models.Model):
    STATUS = {
        ('DRAFT', 'DRAFT'),
        ('PUBLIC', 'PUBLIC'),
    }
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    post = RichTextField(null=True)
    image = ProcessedImageField(
        upload_to='blog',
        format='WEBP', 
        options={'quality': 70},verbose_name="blog image"
    )
    status = models.CharField(choices=STATUS, max_length=10)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True, blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.slug)])

    def increase_views(self):
        self.views += 1
        self.save()


class Tag(models.Model):
    tags = models.CharField(max_length=200)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='tags')
    slug = AutoSlugField(populate_from='tags', unique=True,blank=True,null=True, editable=True)
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tags
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.user.name} on {self.blog.title}"
