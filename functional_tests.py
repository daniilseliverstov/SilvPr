import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class HomePageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        """Проверка title страницы"""
        try:
            self.browser.get("http://localhost:8000")
            self.assertIn("Блоги - Главная страница", self.browser.title)
        except Exception as e:
            self.fail(f"Ошибка при проверке title: {e}")

    def test_home_page_header(self):
        """Проверка корректности Header-a страницы"""
        self.browser.get("http://localhost:8000")
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Лента блогов", header_text)

    def test_home_page_blog_feed(self):
        """
        Проверяет наличие элементов главной страницы:
        1) Контейнер ленты блогов
        """
        self.browser.get("http://localhost:8000")

        try:
            blog_feed = WebDriverWait(self.browser, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "blogs-feed"))
            )
            self.assertTrue(blog_feed.is_displayed())
        except Exception as e:
            self.fail(f'Ошибка при проверке ленты блогов: {str(e)}')

    def test_home_page_content(self):
        """
        Проверяет корректность и содержание ленты блогов:
        1) У блога есть заголовок
        2) У блога есть описание
        3) У блога есть автор
        4) У блога есть категория
        5) У блога есть статья или сообщение об отсутствии статей
        """
        self.browser.get("http://localhost:8000")

        try:
            # Проверяем наличие блогов или сообщения о пустом состоянии
            blog_cards = self.browser.find_elements(By.CLASS_NAME, 'blog-card')
            empty_state = self.browser.find_elements(By.CLASS_NAME, 'empty-state')

            if blog_cards:
                # Если есть блоги, проверяем их содержание
                for blog_card in blog_cards:
                    # Заголовок блога
                    blog_title = blog_card.find_element(By.CLASS_NAME, 'blog-title').text
                    self.assertNotEqual(blog_title, '', 'Заголовок блога пустой')

                    # Описание блога
                    blog_description = blog_card.find_element(By.CLASS_NAME, 'description').text
                    self.assertNotEqual(blog_description, '', 'Описание блога пустое')

                    # Автор блога
                    blog_author = blog_card.find_element(By.CLASS_NAME, 'blog-author').text
                    self.assertNotEqual(blog_author, '', 'Автор блога - пусто')

                    # Категория блога
                    blog_category = blog_card.find_element(By.CLASS_NAME, 'category-tag').text
                    self.assertNotEqual(blog_category, '', 'Пустая категория блога')

                    # Контейнер статей
                    articles_container = blog_card.find_element(By.CLASS_NAME, 'articles-container')

                    # Проверяем статьи или сообщение об отсутствии статей
                    articles = articles_container.find_elements(By.CLASS_NAME, 'article')
                    no_articles_message = articles_container.find_elements(By.CLASS_NAME, 'no-articles')

                    if articles:
                        # Если есть статьи, проверяем их
                        for article in articles:
                            article_title = article.find_element(By.CLASS_NAME, 'article-title').text
                            self.assertNotEqual(article_title, '', 'Заголовок статьи пустой')

                            article_content = article.find_element(By.CLASS_NAME, 'article-content').text
                            self.assertNotEqual(article_content, '', 'Содержание статьи пустое')

                    elif no_articles_message:
                        # Если есть сообщение об отсутствии статей
                        message_text = no_articles_message[0].text
                        self.assertIn('нет опубликованных статей', message_text.lower())

                    else:
                        self.fail('Не найден контейнер статей или сообщение об их отсутствии')

            elif empty_state:
                # Если страница пустая, проверяем сообщение
                empty_text = empty_state[0].text
                self.assertIn('пока нет блогов', empty_text.lower())

            else:
                self.fail('На странице нет ни блогов, ни сообщения о пустом состоянии')

        except Exception as e:
            self.fail(f'Ошибка при проверке контента: {str(e)}')

    def test_home_page_structure(self):
        """Проверяет базовую структуру страницы"""
        self.browser.get("http://localhost:8000")

        # Проверяем основные элементы структуры
        try:
            # Контейнер страницы
            container = self.browser.find_element(By.CLASS_NAME, 'container')
            self.assertTrue(container.is_displayed())

            # Хедер
            header = self.browser.find_element(By.CLASS_NAME, 'header')
            self.assertTrue(header.is_displayed())

            # Лента блогов
            blogs_feed = self.browser.find_element(By.CLASS_NAME, 'blogs-feed')
            self.assertTrue(blogs_feed.is_displayed())

        except Exception as e:
            self.fail(f'Ошибка при проверке структуры страницы: {str(e)}')

    def test_blog_title_is_link_to_blog_page(self):
        """Проверяет, что заголовок блога это ссылка на страницу блога"""
        self.browser.get("http://localhost:8000")

        try:
            blog_cards = self.browser.find_elements(By.CLASS_NAME, 'blog-card')

            if blog_cards:
                first_blog_card = blog_cards[0]
                blog_title_link = first_blog_card.find_element(By.CSS_SELECTOR, '.blog-title a')
                self.assertEqual(blog_title_link.tag_name, 'a', 'Заголовок блога не является ссылкой')

                blog_title_text = blog_title_link.text
                self.assertNotEqual(blog_title_text,'', 'Заголовок блога пустой')

                blog_url = blog_title_link.get_attribute('href')
                self.assertIsNotNone(blog_url, 'У ссылки нет url')

                import re
                match = re.search(r'/blogs/(\d+)/', blog_url)
                if not match:
                    self.fail(f'Неверный формат URL: {blog_url}')
                blog_id = match.group(1)

                blog_title_link.click()
                WebDriverWait(self.browser, 10).until(
                    ec.url_matches(f'http://localhost:8000/blogs/{blog_id}/')
                )

                self.assertEqual(self.browser.current_url, blog_url)
                blog_page_title = self.browser.find_element(By.TAG_NAME, 'h1').text
                self.assertEqual(blog_page_title, blog_title_text)

        except Exception as e:
            self.fail(f'Ошибка при проверке ссылки заголовка блога: {str(e)}')



if __name__ == "__main__":
    unittest.main(verbosity=2)