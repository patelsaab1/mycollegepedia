from rest_framework import serializers
from .models import Blog, Tag,Comment
from General.serializers import OnlyCourseCategorySerializer
from Auth.serializers import BlogProfileSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
        
class CommentSerializer(serializers.ModelSerializer):
    user = BlogProfileSerializer( read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'text', 'created_at']

# class BlogSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True, read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Blog
#         fields = ('id', 'author', 'category', 'title', 'post', 'image', 'status', 'slug', 'published_date', 'views', 'tags', 'comments')



class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class SingleBlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = OnlyCourseCategorySerializer(read_only=True)
    author = BlogProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'author', 'category', 'title', 'post', 'image', 'status', 'slug', 'published_date', 'views', 'tags', 'comments','created_at', 'updated_at','meta_title','meta_keyword','meta_description')

class AdminBlogSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Blog
        fields = '__all__'
        
# Notify
class NotifyBlogSerializer(serializers.ModelSerializer):
    author = BlogProfileSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ('id', 'slug', 'title', 'image','author')