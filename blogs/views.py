from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from blogs.forms import BlogPostForm
from blogs.models import BlogPost
from blogs.services import get_cached_blog
from blogs.utils import slugify


class BlogPostListView(LoginRequiredMixin, ListView):
    """ Список публичных постов блога """
    model = BlogPost
    context_object_name = 'blogposts'
    template_name = 'blogs/blog_list.html'
    permission_required = 'blogs.view_blogpost'

    # paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        """ Фильтрация публичных постов """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        queryset = queryset.order_by('created_at')

        return queryset

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['title'] = 'ПУБЛИКАЦИИ'

        return context


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'blogs/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['blog'] = get_cached_blog(self.object.slug)

        return context

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        blog.view_count += 1
        blog.save()

        return blog


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/blogpost_form.html'
    success_url = reverse_lazy('blogs:blog_list')
    # permission_required = 'blogs.add_blogpost'

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            print(f"Before: Title: {blog.title}, Slug: {blog.slug}")
            blog.slug = slugify(blog.title)
            print(f"After: Title: {blog.title}, Slug: {blog.slug}")
            blog.save()

        return super().form_valid(form)
