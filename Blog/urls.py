from django.urls import path,include
from rest_framework import routers
from .views import BlogListView, BlogDetailView,CommentListCreateView,BlogViewSet,TagViewSet,CommentViewSet,NotifyBlogAPIView

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet,basename='blog')
router.register(r'tags', TagViewSet,basename='tags')
router.register(r'blog-comments', CommentViewSet,basename='blog-comments')
urlpatterns = [
    path('all-blog/', BlogListView.as_view(), name='all_blog'),
    path('blog-detail/<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('comments/', CommentListCreateView.as_view(), name='comments'),
    # Notify
    path('notify-blogs/', NotifyBlogAPIView.as_view(), name='notify-blogs'),
    path('', include(router.urls)),
]
