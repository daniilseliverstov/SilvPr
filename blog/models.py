from tkinter.constants import CASCADE

from django.contrib.auth.models import User
from django.db import models

class Blog(models.Model):
    """Модель Блога"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Article(models.Model):
    """Модель Статей блога"""

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
