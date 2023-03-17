"""Blog2023 URL Configuration"""

from django.contrib import admin
from django.urls import path, include

from django.contrib.sitemaps.views import sitemap  # SiteMap
from news_blog.sitemaps import PostSitemap  # SiteMap

sitemaps = {'posts': PostSitemap, }  # SiteMap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('news_blog.urls', namespace='news_blog')),
    # SiteMap http://127.0.0.1:8001/sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),


]
