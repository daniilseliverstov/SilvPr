from django.shortcuts import render
from .models import Blog, Article


def home_page(request):
    """
    Упрощенное и исправленное представление главной страницы
    """
    blogs = Blog.objects.select_related('author').order_by('-created_at')

    # Для каждого блога находим последнюю опубликованную статью
    for blog in blogs:
        last_article = blog.articles.filter(status='published').order_by('-created_at').first()
        if last_article:
            blog.last_article_title = last_article.title
            blog.last_article_content = last_article.content
            blog.last_article_created = last_article.created_at
        else:
            blog.last_article_title = None
            blog.last_article_content = None
            blog.last_article_created = None

    return render(request, 'home_page.html', {'blogs': blogs})