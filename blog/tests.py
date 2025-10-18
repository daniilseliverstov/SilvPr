
from django.http import HttpRequest
from django.test import TestCase
from blog.models import Blog

from datetime import datetime

from blog.views import home_page


class HomePageTest(TestCase):
    """Класс для тестирования домашней страницы"""

    def test_home_page_returns_correct_html(self):
        """Проверяет херню, мб переделать"""
        response = self.client.get("/")
        self.assertContains(response, "<title> Блоги </title>")
        self.assertContains(response, "<h1> Лента блогов </h1>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")

    def test_home_page_display_blog(self):
        """Проверяет верное отображение блога на странице"""

        Blog.objects.create(
            title="title1",
            description="description1",
            category="category1",
            created_at=datetime.now()
        )

        Blog.objects.create(
            title="title2",
            description="description2",
            category="category2",
            created_at=datetime.now()
        )

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')

        self.assertIn('title1', html)
        self.assertIn('description1', html)
        self.assertIn('category1', html)

        self.assertIn('title2', html)
        self.assertIn('description2', html)
        self.assertIn('category2', html)

class BlogModelTest(TestCase):

    def test_blog_save_and_retrieve(self):
        """Проверяет как создается блог"""
        blog1 = Blog(
            title = "Blog_1",
            description = "description_1",
            created_at = datetime.now(),
            category = "category_1",
        )
        blog2 = Blog(
            title="Blog_2",
            description="description_2",
            created_at=datetime.now(),
            category="category_2",
        )
        blog1.save()
        blog2.save()

        all_blogs = Blog.objects.all()
        self.assertEqual(len(all_blogs), 2)

        self.assertEqual(blog1.title, all_blogs[0].title)
        self.assertEqual(blog2.title, all_blogs[1].title)

