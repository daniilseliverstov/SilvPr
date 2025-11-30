from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
]