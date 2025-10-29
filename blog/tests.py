
from django.http import HttpRequest
from django.test import TestCase
from blog.models import Blog
from blog.models import Article
from django.contrib.auth.models import User

from datetime import datetime

from blog.views import home_page


class HomePageTest(TestCase):
    """Класс для тестирования домашней страницы"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='test-user',
            password='test-password'
        )

    def test_home_page_returns_correct_html(self):
        """Проверяет херню, мб переделать"""
        response = self.client.get("/")
        self.assertContains(response, "<title> Блоги </title>")
        self.assertContains(response, "<h1> Лента блогов </h1>")
        self.assertContains(response, '<html lang="ru">')
        self.assertContains(response, "</html>")

    def test_home_page_display_blog(self):
        """Проверяет верное отображение постов на странице"""

        blog1 = Blog.objects.create(
            title="title1",
            description="description1",
            category="category1",
            created_at=datetime.now(),
            author=self.user
        )

        blog2 = Blog.objects.create(
            title="title2",
            description="description2",
            category="category2",
            created_at=datetime.now(),
            author=self.user
        )

        article1 = Article.objects.create(
            blog=blog1,
            title='Первая статья, опубликована',
            content='Содержание первой статьи',
            status='published'
        )
        article2 = Article.objects.create(
            blog=blog1,
            title='Вторая статья, черновик, не виден',
            content='Содержание второй статьи',
            status='draft'
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

        self.assertIn('test-user', html)

        self.assertIn('Первая статья, опубликована', html)
        self.assertIn('Содержание первой статьи', html)
        self.assertNotIn('Вторая статья, черновик, не виден', html)
        self.assertNotIn('Содержание второй статьи', html)

class BlogModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test-user',
            password='testpass123'
        )

    def test_blog_save_and_retrieve(self):
        """Проверяет как создается блог"""
        blog1 = Blog(
            title="Blog_1",
            description="description_1",
            created_at=datetime.now(),
            category="category_1",
            author=self.user,
        )
        blog2 = Blog(
            title="Blog_2",
            description="description_2",
            created_at=datetime.now(),
            category="category_2",
            author=self.user,
        )
        blog1.save()
        blog2.save()

        all_blogs = Blog.objects.all()
        self.assertEqual(len(all_blogs), 2)

        self.assertEqual(blog1.title, all_blogs[0].title)
        self.assertEqual(blog2.title, all_blogs[1].title)
        self.assertEqual(all_blogs[0].author, self.user)
        self.assertEqual(all_blogs[1].author, self.user)
        self.assertEqual(all_blogs[0].category, blog1.category)
        self.assertEqual(all_blogs[1].category, blog2.category)




class ArticleModelTest(TestCase):
    """Тесты для модели Article"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blog = Blog.objects.create(
            title='Тестовый блог',
            description='Описание',
            category='Категория',
            author=self.user,
            created_at=datetime.now()
        )

    def test_article_save_and_retrieve(self):
        """Проверка создания и получения статей"""

        article1 = Article.objects.create(
            blog=self.blog,
            title='Статья1',
            content='Содержание1',
            status='published'
        )
        article2 = Article.objects.create(
            blog=self.blog,
            title="Статья 2",
            content="Содержание 2",
            status='draft'
        )

        all_articles = Article.objects.all()
        self.assertEqual(len(all_articles), 2)
        self.assertEqual(article1.title, all_articles[0].title)
        self.assertEqual(article2.title, all_articles[1].title)

        blog_article = self.blog.articles.all()
        self.assertEqual(len(blog_article), 2)


