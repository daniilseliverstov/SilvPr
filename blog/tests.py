from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from blog.models import Blog
from blog.models import Article
from datetime import datetime, timedelta
from django.contrib.auth.models import User



class HomePageTest(TestCase):
    """
    Набор тестов для проверки функциональности главной страницы приложения.

    Тесты охватывают отображение блогов, статей, корректность HTML-структуры
    и наличие навигационных ссылок.
    """

    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.

        Создает тестового пользователя, который будет использоваться
        как автор блогов и статей в последующих тестах.
        """
        self.user = User.objects.create_user(
            username='test-user',
            password='test-password'
        )

    def test_home_page_returns_correct_html(self):
        """
        Комплексная проверка HTML-структуры главной страницы.

        Проверяет корректность разметки, наличие ключевых элементов
        и базовую функциональность страницы.

        Это гарантирует, что страница загружается без критических ошибок разметки.
        """
        response = self.client.get("/")

        # Базовые проверки ответа
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page.html')

        # Критически важные HTML-элементы
        self.assertContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "<html lang=\"ru\">")
        self.assertContains(response, "</html>")
        self.assertContains(response, "<title>Блоги - Главная страница</title>")

        # Мета-теги для корректного отображения
        self.assertContains(response, 'meta charset="UTF-8"')
        self.assertContains(response, 'viewport')
        self.assertContains(response, 'width=device-width, initial-scale=1.0')

        # Семантическая структура - главный заголовок
        self.assertContains(response, "<h1>")
        self.assertContains(response, "Лента блогов")

        # Ключевые контейнеры для контента
        self.assertContains(response, 'class="container"')
        self.assertContains(response, 'class="header"')
        self.assertContains(response, 'class="blogs-feed"')

        # Подключение стилей
        self.assertContains(response, 'link rel="stylesheet"')
        self.assertContains(response, 'static/css/style.css')


    def test_home_page_display_blog(self):
        """
        Комплексная проверка отображения блогов и их контента на главной странице.

        Тест проверяет:
        - Отображение заголовков, описаний и категорий блогов
        - Корректное отображение информации об авторе
        - Фильтрацию статей по статусу (только опубликованные)
        - Наличие кликабельных ссылок в заголовках блогов

        Особое внимание уделяется:
        - Видимости опубликованных статей и скрытию черновиков
        - Правильному формированию URL для страниц отдельных блогов
        - Соответствию текста ссылок заголовкам блогов
        """

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

        self.assertIn(f'<a href="/blogs/{blog1.id}/">', html)
        self.assertIn(f'<a href="/blogs/{blog2.id}/">', html)
        self.assertIn(f'>{blog1.title}</a>', html)
        self.assertIn(f'>{blog2.title}</a>', html)


class BlogModelTest(TestCase):
    """
    Тесты для модели Blog, проверяющие корректность работы с данными блогов.

    Включает тесты создания, сохранения, извлечения и отображения блогов.
    """

    def setUp(self):
        """
        Инициализация тестового пользователя для создания блогов.
        """
        self.user = User.objects.create_user(
            username='test-user',
            password='testpass123'
        )

    def test_blog_save_and_retrieve(self):
        """
        Проверяет механизм сохранения и извлечения блогов из базы данных.

        Тест проверяет:
        - Корректное сохранение блогов в базу данных
        - Полное извлечение всех созданных блогов
        - Сохранение всех атрибутов блога (заголовок, описание, категория)
        - Правильную связь блога с автором (User)

        Это гарантирует целостность данных и корректность ORM-операций.
        """
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

        blog_titles = [blog.title for blog in all_blogs]
        self.assertIn("Blog_1", blog_titles)
        self.assertIn("Blog_2", blog_titles)

        self.assertEqual(all_blogs[0].author, self.user)
        self.assertEqual(all_blogs[1].author, self.user)

    def test_home_page_displays_last_published_article(self):
        """
        Проверяет логику отображения последней опубликованной статьи для каждого блога.

        Тест создает несколько статей с разными статусами и датами публикации,
        чтобы проверить:
        - Отображение только последней опубликованной статьи
        - Игнорирование статей со статусом "черновик"
        - Игнорирование устаревших опубликованных статей
        - Корректную работу сортировки по дате создания

        Это гарантирует, что пользователи видят только актуальный контент.
        """

        blog = Blog.objects.create(
            title="Тестовый блог",
            description="Описание тестового блога",
            category="Тестовая категория",
            created_at=datetime.now(),
            author=self.user
        )

        now = timezone.now()

        old_article = Article.objects.create(
            blog=blog,
            title='Старая статья',
            content='Содержание старой статьи',
            status='published',
            created_at=now - timedelta(days=2)
        )

        import time
        time.sleep(0.1)

        draft_article = Article.objects.create(
            blog=blog,
            title='Черновик статьи',
            content='Содержание черновика',
            status='draft',
            created_at=now - timedelta(days=1)
        )

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

        self.assertIn('Новая статья', html)
        self.assertIn('Содержание новой статьи', html)

        self.assertNotIn('Старая статья', html)
        self.assertNotIn('Содержание старой статьи', html)

        self.assertNotIn('Черновик статьи', html)
        self.assertNotIn('Содержание черновика', html)


class ArticleModelTest(TestCase):
    """
    Тесты для модели Article, проверяющие работу со статьями блогов.

    Включает тесты создания статей, связей с блогами и базовых операций с данными.
    """

    def setUp(self):
        """
        Подготовка тестового окружения: пользователь и блог для статей.
        """
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
        """
        Проверяет создание, сохранение и извлечение статей из базы данных.

        Тест проверяет:
        - Корректное сохранение статей с различными статусами
        - Полноту извлечения всех созданных статей
        - Наличие связей между статьями и родительскими блогами
        - Корректность обратных связей (related_name)

        Это обеспечивает надежность работы с иерархией данных блог-статья.
        """

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

        article_titles = [article.title for article in all_articles]
        self.assertIn('Статья1', article_titles)
        self.assertIn('Статья 2', article_titles)

        blog_article = self.blog.articles.all()
        self.assertEqual(len(blog_article), 2)


class BlogsPageTest(TestCase):
    """
    Тесты для страницы детального просмотра блога.

    Проверяет функциональность страницы, которая открывается
    при клике на заголовок блога на главной странице.
    """

    def setUp(self):
        """
        Подготовка тестовых данных - блог со статьями
        """
        self.user = User.objects.create_user(
            username='test-author',
            password='test-password'
        )

        self.blog = Blog.objects.create(
            title="Тестовый блог для детальной страницы",
            description="Подробное описание тестового блога",
            category="Тестирование",
            created_at=datetime.now(),
            author=self.user
        )

        self.published_article1 = Article.objects.create(
            blog=self.blog,
            title="Первая опубликованная статья",
            content="Содержание первой опубликованной статьи",
            status='published',
            created_at=datetime.now() - timedelta(days=2)
        )

        self.published_article2 = Article.objects.create(
            blog=self.blog,
            title="Вторая опубликованная статья",
            content="Содержание второй опубликованной статьи",
            status='published',
            created_at=datetime.now() - timedelta(days=1)
        )

        self.draft_article = Article.objects.create(
            blog=self.blog,
            title="Черновик статьи (не должен отображаться)",
            content="Содержание черновика",
            status='draft',
            created_at=datetime.now()
        )

    def test_blog_detail_page_returns_correct_html(self):
        """
        Проверяет корректность HTML-структуры страницы блога.
        """
        response = self.client.get(f"/blogs/{self.blog.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_detail.html')

        self.assertContains(response, "<!DOCTYPE html>")
        self.assertContains(response, f"<title>{self.blog.title} - Блог</title>")
        self.assertContains(response, self.blog.title)
        self.assertContains(response, self.blog.description)
        self.assertContains(response, self.blog.category)

    # def test_blog_detail_page_displays_blog_info(self):
    #     """
    #     Проверяет отображение всей информации о блоге.
    #     """
    #     response = self.client.get(f"/blogs/{self.blog.id}/")
    #     html = response.content.decode('utf-8')
    #
    #     self.assertIn(self.blog.title, html)
    #     self.assertIn(self.blog.description, html)
    #     self.assertIn(self.blog.category, html)
    #     self.assertIn(self.user.username, html)
    #
    #     self.assertIn(self.blog.created_at.strftime("%d.%m.%Y"), html)
    #
    # def test_blog_detail_page_displays_only_published_articles(self):
    #     """
    #     Проверяет что отображаются только опубликованные статьи.
    #     """
    #     response = self.client.get(f"/blogs/{self.blog.id}/")
    #     html = response.content.decode('utf-8')
    #
    #     self.assertIn(self.published_article1.title, html)
    #     self.assertIn(self.published_article1.content, html)
    #     self.assertIn(self.published_article2.title, html)
    #     self.assertIn(self.published_article2.content, html)
    #
    #     self.assertNotIn(self.draft_article.title, html)
    #     self.assertNotIn(self.draft_article.content, html)
    #
    # def test_blog_detail_page_articles_ordering(self):
    #     """
    #     Проверяет правильную сортировку статей (новые сверху).
    #     """
    #     response = self.client.get(f"/blogs/{self.blog.id}/")
    #     html = response.content.decode('utf-8')
    #
    #     article2_pos = html.find(self.published_article2.title)
    #     article1_pos = html.find(self.published_article1.title)
    #
    #     self.assertLess(article2_pos, article1_pos,
    #                     "Статьи должны быть отсортированы от новых к старым")
    #
    # def test_blog_detail_page_back_link(self):
    #     """
    #     Проверяет наличие ссылки для возврата на главную страницу
    #     """
    #     response = self.client.get(f"/blogs/{self.blog.id}/")
    #     html = response.content.decode('utf-8')
    #
    #     self.assertIn('href="/"', html)
    #     self.assertIn('Назад к ленте блогов', html)
    #
    # def test_blog_detail_page_nonexistent_blog_returns_404(self):
    #     """
    #     Проверяет что запрос несуществующего блога возвращает 404.
    #     """
    #     response = self.client.get("/blogs/abc/")
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_blog_detail_page_empty_blog_displays_message(self):
    #     """
    #     Проверяет отображение сообщения когда в блоге нет статей.
    #     """
    #     # Создаем пустой блог
    #     empty_blog = Blog.objects.create(
    #         title="Пустой блог",
    #         description="Блог без статей",
    #         category="Тестирование",
    #         created_at=datetime.now(),
    #         author=self.user
    #     )
    #
    #     response = self.client.get(f"/blogs/{empty_blog.id}/")
    #     html = response.content.decode('utf-8')
    #
    #     self.assertIn('нет опубликованных статей', html.lower())
    #
    # def test_blog_detail_page_url_matches_home_page_links(self):
    #     """
    #     Проверяет что URL страницы блога соответствует ссылкам на главной.
    #     """
    #     home_response = self.client.get("/")
    #     home_html = home_response.content.decode('utf-8')
    #
    #     expected_url = f'/blogs/{self.blog.id}/'
    #     self.assertIn(f'href="{expected_url}"', home_html)
    #
    #     detail_response = self.client.get(expected_url)
    #     self.assertEqual(detail_response.status_code, 200)
    #     self.assertIn(self.blog.title, detail_response.content.decode('utf-8'))