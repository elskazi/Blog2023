from django.contrib import admin

from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)} #   поле «slug» заполняется автоматически
    raw_id_fields = ('author',)  # появляется поиск рядом с Автором, типа что б неебаться
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
