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
        """
        self.browser.get("http://localhost:8000")

        try:

            article_title= self.browser.find_element(By.CLASS_NAME, 'blog-title').text
            self.assertNotEqual(article_title, '')

            article_summary = self.browser.find_element(By.CLASS_NAME, 'description').text
            self.assertNotEqual(article_summary, '')

        except Exception as e:
            self.fail(f'Ошибка при проверке контента: {str(e)}')


if __name__ == "__main__":  
    unittest.main(verbosity=2)