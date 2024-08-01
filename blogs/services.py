from django.core.cache import cache

from blogs.models import BlogPost
from config import settings


def get_cached_blog(slug):
    # кеширование на 15 минут
    cache_timeout = 60 * 15
    cache_key = slug

    if settings.CACHE_ENABLED:
        blog = cache.get_or_set(cache_key, cache_timeout)

        if not blog:
            blog = BlogPost.objects.get(slug=slug),
            cache.add(cache_key, blog, cache_timeout)
    else:
        blog = BlogPost.objects.get(slug=slug)

    print(f'Кэширование блога {slug}')
    return blog
