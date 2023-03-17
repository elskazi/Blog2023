from django.contrib.sitemaps import Sitemap
from .models import Post
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    '''Метод items() возвращает QuerySet объектов, которые будут отображаться в карте сайта. По умолчанию Django использует метод get_absolute_url()
    объектов списка, чтобы получать их URL’ы.'''
    def items(self):
        return Post.published.all()
    ''' Метод lastmod принимает каждый объект из результата вызова items() и возвращает время последней модификации
    статьи.'''
    def lastmod(self, obj):
        return obj.updated