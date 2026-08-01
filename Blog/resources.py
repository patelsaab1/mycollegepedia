from import_export import resources
from .models import Blog

class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog
        fields = ('id','title','category__name','author__name','post','image','views','status','published_date','created_at','updated_at','meta_title','meta_keyword','meta_description','slug')