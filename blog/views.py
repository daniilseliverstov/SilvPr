from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return HttpResponse("""
                        <html><title> SilvPr </title></html>
                        <h1> Сайт SilvPr </h1>
                        """)
