from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe #  фильтр для разрашения ХТМЛ
import markdown # Подключаем установленный маркдаун


register = template.Library()

#simple_tag – обрабатывает данные и возвращает строку;
@register.simple_tag()  #(name='my_tag')  # можно задать имя, а так как имя функции
def total_posts():
    return Post.published.count()

# inclusion_tag – обрабатывает данные и возвращает сформированный фрагмент шаблона.
# с использованием отдельного шаблона для перебора
@register.inclusion_tag('news_blog/post/latest_posts.html')
def show_latest_posts(count=5):  # кол-во можем передавать в шаблоне после тега
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# Без использованием  шаблона , перебор в шаблоне сайта
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

# Фильтр так же, как регистрировали теги
@register.filter(name='markdown') # дали имя так могли быть конфликты если б назвали функции как данное имя
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
