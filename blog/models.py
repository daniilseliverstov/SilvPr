from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Blog(models.Model):
    """Модель Блога"""
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    category = models.CharField(max_length=100, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

    @property
    def published_articles_count(self):
        """Количество опубликованных статей в блоге"""
        return self.articles.filter(status='published').count()

    def get_last_published_article(self):
        """Последняя опубликованная статья"""
        return self.articles.filter(status='published').order_by('-created_at').first()


class Article(models.Model):
    """Модель Статей блога"""

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    ]

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Блог"
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    @property
    def is_published(self):
        """Проверка, опубликована ли статья"""
        return self.status == 'published'

    def publish(self):
        """Опубликовать статью"""
        self.status = 'published'
        self.save()

    def unpublish(self):
        """Перевести в черновик"""
        self.status = 'draft'
        self.save()