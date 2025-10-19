from django.db import models

class Blog(models.Model):
    """Модель Блога"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    created_at =models.DateTimeField()

