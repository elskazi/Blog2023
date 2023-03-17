from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView  # вернули старый вид
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # древняя погинация
from .forms import EmailPostForm, CommentForm, SearchForm  # форма отправки на мыло, Comments, Search
from django.core.mail import send_mail  # служба отправки почты
from taggit.models import Tag  # Теги
from django.db.models import Count
from .models import Post, Comment
from django.contrib.postgres.search import SearchVector # поиск по нескольким полям
from django.contrib.postgres.search import SearchQuery, SearchRank # Поиск с ранжированием, по заголовку потом по тексту
from django.contrib.postgres.search import TrigramSimilarity , TrigramDistance, TrigramWordDistance # Поиск, даже с опечаткой

from django.views.decorators.http import require_POST # для новой версии комметов

# class PostListView(ListView ):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'news_blog/post/list.html'


########## Выключили потом включили, так как используем ТЭГИ
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None  # tags
    if tag_slug:  # tags
        tag = get_object_or_404(Tag, slug=tag_slug)  # tags
        object_list = object_list.filter(tags__in=[tag])  # tags

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, доставить первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница выходит за пределы допустимого диапазона, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'news_blog/post/list.html',
                  {'page': page,
                   'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    ''' выключили старую обработку коментов '''
    # # Список активных комментариев для этой статьи.
    # comments = post.comments.filter(active=True)
    # new_comment = None
    # if request.method == 'POST':
    #     # Пользователь отправил комментарий.
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         # Создаем комментарий, но пока не сохраняем в базе данных.
    #         new_comment = comment_form.save(commit=False)
    #         # Привязываем комментарий к текущей статье.
    #         new_comment.post = post
    #         # Сохраняем комментарий в базе данных.
    #         new_comment.save()
    # else:
    #     comment_form = CommentForm()

    # Формирование списка похожих статей.
    post_tags_ids = post.tags.values_list('id', flat=True)  # получает все ID тегов текущей статьи.
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
        id=post.id)  # получить статьи по тегам, искючить текущую
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]  # считаем, сотируем, срезаем
    return render(request, 'news_blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        # 'new_comment': new_comment,  #выключили старую обработку коментов
        # 'comment_form': comment_form, #выключили старую обработку коментов
        'similar_posts': similar_posts})

# Комметарии новая версия (убрали из post_detail )
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'news_blog/post/comment.html',
    {'post': post,
    'form': form,
    'comment': comment})



# Отправка почты
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомндует "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'elskazi@yandex.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'news_blog/post/share.html', {'post': post,
                                                         'form': form,
                                                         'sent': sent})




###### Далее идет тестирования способов поиска #########

# Поиск1 ...  была ошибка, Post.object.annotate а не Post.objectS.annotate
def post_search1(request):  # Выкл
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.object.annotate(search=SearchVector('title', 'body')).filter(search=query) # Post.objectS.annotate
    return render(request, 'news_blog/post/search.html', {'form': form, 'query': query, 'results': results})

# Поиск2 Стемминг и ранжирование результатов
def post_search2(request): # Выкл
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.object.annotate(search=search_vector,
                rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    return render(request, 'news_blog/post/search.html', {'form': form, 'query': query, 'results': results})


# Поиск3 Взвешенные запросы
def post_search3(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.object.annotate(rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    return render(request, 'news_blog/post/search.html', {'form': form, 'query': query, 'results': results})



# Поиск4 Если опучатка, лучший надо устновить расширение в ПГАдмин
# CREATE EXTENSION pg_trgm
#TrigramSimilarity  дробит на слова по отдельности
#TrigramWordSimilarity найти кусок слова
#TrigramWordDistance
#
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
            # не ведомая ебанина, ищет все :
            #results = Post.object.annotate(distance=TrigramWordDistance(query , 'title'),
            #).filter(distance__gt=0.3).order_by('-distance')
    return render(request, 'news_blog/post/search.html', {'form': form, 'query': query, 'results': results})