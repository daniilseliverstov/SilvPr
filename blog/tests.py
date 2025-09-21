from django.test import TestCase
from django.http import HttpRequest
from blog.views import home_page
from blog.models import Blog


class HomePageTest(TestCase):
    """Класс для тестирования домашней страницы"""

    def test_home_page_returns_correct_html(self):
        """Проверяет херню, мб переделать"""
        response = self.client.get("/")
        self.assertContains(response, "<title> Блоги </title>")
        self.assertContains(response, "<h1> Лента блогов </h1>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")


class BlogModelTest(TestCase):

    def test_blog_save_and_retrieve(self):
        """Проверяет как создается блог"""
        blog1 = Blog(
            title = "",

        )
        blog2 = Blog()
        blog1.save()
        blog2.save()
