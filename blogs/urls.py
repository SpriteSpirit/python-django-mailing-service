from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BlogPostListView, BlogPostCreateView

app_name = 'catalog'

timeout20min = 60*20
timeout10min = 60*10
timeout20sec = 20
timeout10sec = 10

urlpatterns = [
    # path('', index.as_view(), name='home'),
    path('blogs/', BlogPostListView.as_view(), name='blog_list'),
    path('create_blog/', BlogPostCreateView.as_view(), name='create_blog'),
]