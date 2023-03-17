from django.conf.urls import *
from django.urls import path
from . import views
from .feeds import LatestPostsFeed  # Добавление rSS Для статей

app_name = 'news_blog'

urlpatterns = [
    # список постов, включили оборатно из-за Тегов (вместо views.PostListView.as_view())
    path('', views.post_list, name='post_list'),
    # обратиться к списку статей, связанных с определенным тегом
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # список постов, выкл из-за Тегов, так как вроде не работают с  ListView
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    # отправка почты
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # Добавление rSS Для статей  http://127.0.0.1:8001/blog/feed/
    path('feed/', LatestPostsFeed(), name='post_feed'),
    # Поиск
    path('search/', views.post_search, name='post_search'),
    # Комметрии обновленная версия
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

]
