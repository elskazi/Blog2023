from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Достаем всех юзеров
from django.urls import reverse #  создавать URL-адреса по их имени и передавать необязательные параметры
from taggit.managers import TaggableManager # теги доп пакет



# Переопределение менеджера модели вместо objects будет published
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )

    # Правильный вид чойсов, а не тот что выше...  влом переписывать
    # class Status(models.TextChoices):
    #     DRAFT = 'DF', 'Draft'
    #     PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # related_name избавляемся от author_set теперь author.blog_posts.all()
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    object= models.Manager() # Переопределение менеджера модели
    published = PublishedManager() # Переопределение менеджера модели
    tags = TaggableManager() # теги доп пакет

    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def get_absolute_url(self):
        ''' Кононические УРЛ '''
        return reverse('news_blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,  # без нулей
                             self.publish.strftime('%d'), # с нулями
                             self.slug])

    def __str__(self):
        return self.title


# Comments
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # related_name избавляемся от comment_set теперь  post.comments.all()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)