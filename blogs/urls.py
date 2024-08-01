from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BlogPostListView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'catalog'

timeout20min = 60*20
timeout10min = 60*10
timeout20sec = 20
timeout10sec = 10

urlpatterns = [
    path('blogs/', BlogPostListView.as_view(), name='blog_list'),
    path('create_blog/', BlogPostCreateView.as_view(), name='create_blog'),
    path('detail_blog/<slug:slug>/', BlogPostDetailView.as_view(), name='detail_blog'),
    path('update_blog/<slug:slug>/', BlogPostUpdateView.as_view(), name='update_blog'),
    path('delete_blog/<slug:slug>/', BlogPostDeleteView.as_view(), name='delete_blog'),
]
