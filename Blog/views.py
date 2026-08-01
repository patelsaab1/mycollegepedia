from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django_filters import rest_framework as filters
from .models import Blog, Tag,Comment
from .serializers import BlogSerializer, SingleBlogSerializer, TagSerializer,CommentSerializer,AdminBlogSerializer,NotifyBlogSerializer
from rest_framework.filters import SearchFilter
from General.permissions import IsCollege
from rest_framework import viewsets, generics
from datetime import timedelta
from django.db import models
from django.utils import timezone

# Create your views here.

# class BlogListView(ListAPIView):
#     # queryset = Blog.objects.all()
#     serializer_class = SingleBlogSerializer
#     permission_classes = (AllowAny,)
    
#     def get_queryset(self):
#         return Blog.objects.filter(status='PUBLIC')


class BlogListFilter(filters.FilterSet):
    class Meta:
        model = Blog
        fields = {'category': ['exact']}

class BlogListView(ListAPIView):
    queryset = Blog.objects.filter(status='PUBLIC')
    serializer_class = SingleBlogSerializer
    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,SearchFilter)
    filterset_class = BlogListFilter
    search_fields = ['title', 'category__name',  'author__name',]

class BlogDetailView(RetrieveAPIView):
    queryset = Blog.objects.filter(status='PUBLIC')
    serializer_class = SingleBlogSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_object(self):
        blog = super().get_object()
        # Increase views when the blog is accessed
        blog.increase_views()
        return blog
        
        
class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Notify
class NotifyBlogAPIView(ListAPIView):
    serializer_class = NotifyBlogSerializer

    def get_queryset(self):
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())

        queryset = Blog.objects.filter(
            models.Q(created_at__gte=start_of_week) |
            models.Q(updated_at__gte=start_of_week)
        )
        return queryset

# College Dashboard

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = AdminBlogSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    lookup_field = 'slug'
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Blog.objects.filter(author=user)
        else:
            return Blog.objects.none()

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get', 'post', 'put', 'patch','delete']
    lookup_field = 'slug'
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated :
            return Tag.objects.filter(blog__author=user)
        else:
            return Tag.objects.none()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,IsCollege]
    http_method_names = ['get','delete']
    lookup_field = 'slug'
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated :
            return Comment.objects.filter(blog__author=user)
        else:
            return Comment.objects.none()

# class CollegeViewSet(viewsets.ModelViewSet):
#     queryset = College.objects.all()
#     serializer_class = CollegeSerializer
#     permission_classes = [IsAuthenticated,IsCollege]
#     http_method_names = ['get', 'post', 'put', 'patch',]
#     lookup_field = 'slug'
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return College.objects.filter(college_user=user)
#         else:
#             return College.objects.none()


