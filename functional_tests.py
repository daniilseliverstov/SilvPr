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
            self.assertIn("Блоги", self.browser.title)
        except Exception as e:
            self.fail(f"Ошибка при проверке title {e}")

    def test_home_page_header(self):
        """Проверка корректности Header-a страницы"""
        self.browser.get("http://localhost:8000")
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Лента блогов", header_text)

    def test_home_page_blog(self):
        """
        Проверяет наличие элементов главной станицы:

        1) Список постов

        """
        self.browser.get("http://localhost:8000")

        try:
            article_PL = WebDriverWait(self.browser, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "post-list"))
            )
            self.assertTrue(article_PL.is_displayed())
        except Exception as e:
            self.fail(f'Ошибка при проверке списка постов: {str(e)}')

    def test_home_page_content(self):
        """
        Проверяет корректность и содержание ленты блогов:

        1) У Блога есть заготовок
        2) У Блога есть описание
        3) У блога есть автор
        4) У блога есть категория
        5) У блога есть статья
        """
        self.browser.get("http://localhost:8000")


        try:
            posts = self.browser.find_elements(By.CLASS_NAME, 'post')
            self.assertGreater(len(posts), 0, 'На странице нет блогов')

            for post in posts:

                blog_title= self.browser.find_element(By.CLASS_NAME, 'blog-title').text
                self.assertNotEqual(blog_title, '', 'Заголовок блога пустой')

                blog_description = self.browser.find_element(By.CLASS_NAME, 'description').text
                self.assertNotEqual(blog_description, '', 'Описание блога пустое')

                blog_author = self.browser.find_element(By.CLASS_NAME, 'blog-author').text
                self.assertNotEqual(blog_author, '', 'Автор блога - пусто')

                blog_category = self.browser.find_element(By.CLASS_NAME, 'category-tag').text
                self.assertNotEqual(blog_category, '', 'Пустая категория блога')

                articles_container = post.find_element(By.CLASS_NAME, 'articles-container')
                try:
                    articles = articles_container.find_elements(By.CLASS_NAME, 'articles')
                    if len(articles) > 0:
                        for article in articles:
                            article_title = article.find_element(By.CLASS_NAME, 'article-title').text
                            self.assertNotEqual(article_title, '', 'Заголовок статьи пустой')
                            article_content = article.find_element(By.CLASS_NAME, 'article-content').text
                            self.assertNotEqual(article_content, '', 'Содержание статьи пустое')
                    else:
                        no_articles_message = articles_container.find_element(By.CLASS_NAME, 'no-articles').text
                        self.assertEqual(no_articles_message, 'Блог без статей')
                except Exception as ex:
                    self.fail(f'Ошибка при проверке статейЖ {str(ex)}')

        except Exception as e:
            self.fail(f'Ошибка при проверке контента: {str(e)}')


if __name__ == "__main__":  
    unittest.main(verbosity=2)