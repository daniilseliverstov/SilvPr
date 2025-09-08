from django.test import TestCase
from django.http import HttpRequest
from blog.views import home_page


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertContains(response, "<title> SilvPr </title>")
        self.assertContains(response, "<h1> Сайт SilvPr </h1>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")