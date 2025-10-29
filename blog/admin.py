from django.contrib import admin

from .models import Blog, Article


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
