from django.http import HttpResponse
from .models import Blog
from django.shortcuts import render


def home_page(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request,'home_page.html', context)
