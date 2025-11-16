from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from blog.models import Blog
from blog.models import Article
from datetime import datetime, timedelta
from django.contrib.auth.models import User

from blog.views import home_page


class HomePageTest(TestCase):
    """Класс для тестирования домашней страницы"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='test-user',
            password='test-password'
        )

    def test_home_page_returns_correct_html(self):
        """Проверяет корректность HTML-структуры главной страницы"""
        response = self.client.get("/")
        # Обновил проверки под новый шаблон
        self.assertContains(response, "<title>Блоги - Главная страница</title>")
        self.assertContains(response, "Лента блогов")
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

        response = self.client.get("/")
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
        blog1 = Blog.objects.create(
            title="Blog_1",
            description="description_1",
            created_at=datetime.now(),
            category="category_1",
            author=self.user,
        )
        blog2 = Blog.objects.create(
            title="Blog_2",
            description="description_2",
            created_at=datetime.now(),
            category="category_2",
            author=self.user,
        )

        all_blogs = Blog.objects.all()
        self.assertEqual(len(all_blogs), 2)

        # Проверяем что оба блога существуют, не зависимо от порядка
        blog_titles = [blog.title for blog in all_blogs]
        self.assertIn("Blog_1", blog_titles)
        self.assertIn("Blog_2", blog_titles)

        self.assertEqual(all_blogs[0].author, self.user)
        self.assertEqual(all_blogs[1].author, self.user)

    def test_home_page_displays_last_published_article(self):
        """Проверяет, что для каждого блога отображается последняя опубликованная статья"""

        blog = Blog.objects.create(
            title="Тестовый блог",
            description="Описание тестового блога",
            category="Тестовая категория",
            created_at=datetime.now(),
            author=self.user
        )

        now = timezone.now()

        # Создаем статьи с задержкой, чтобы гарантировать порядок
        old_article = Article.objects.create(
            blog=blog,
            title='Старая статья',
            content='Содержание старой статьи',
            status='published',
            created_at=now - timedelta(days=2)
        )

        # Ждем секунду чтобы гарантировать разницу во времени
        import time
        time.sleep(0.1)

        draft_article = Article.objects.create(
            blog=blog,
            title='Черновик статьи',
            content='Содержание черновика',
            status='draft',
            created_at=now - timedelta(days=1)
        )

        # Еще ждем
        time.sleep(0.1)

        latest_article = Article.objects.create(
            blog=blog,
            title='Новая статья',
            content='Содержание новой статьи',
            status='published',
            created_at=now
        )

        response = self.client.get("/")
        html = response.content.decode('utf-8')

        # Должна отображаться НОВАЯ статья (последняя опубликованная)
        self.assertIn('Новая статья', html)
        self.assertIn('Содержание новой статьи', html)

        # Старая статья НЕ должна отображаться (только последняя)
        self.assertNotIn('Старая статья', html)
        self.assertNotIn('Содержание старой статьи', html)

        # Черновики никогда не отображаются
        self.assertNotIn('Черновик статьи', html)
        self.assertNotIn('Содержание черновика', html)


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

        # Проверяем что обе статьи существуют, не зависимо от порядка
        article_titles = [article.title for article in all_articles]
        self.assertIn('Статья1', article_titles)
        self.assertIn('Статья 2', article_titles)

        blog_article = self.blog.articles.all()
        self.assertEqual(len(blog_article), 2)