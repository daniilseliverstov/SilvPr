from django.shortcuts import render, get_object_or_404
from .models import Blog, Article


def home_page(request):
    """
    Gредставление главной страницы
    """
    blogs = Blog.objects.select_related('author').order_by('-created_at')


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


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    articles = blog.articles.filter(status='published').order_by('-created_at')
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'articles': articles
    })