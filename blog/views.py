from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return HttpResponse("""
                        <html><title> Блоги </title></html>
                        <h1> Лента блогов </h1>
                        """)
