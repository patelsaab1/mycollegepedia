from import_export import resources
from .models import *

class CollegeResource(resources.ModelResource):
    class Meta:
        model = College
        # fields = ('id','title','category__name','author__name','post','image','views','status','published_date','created_at','updated_at','meta_title','meta_keyword','meta_description','slug')