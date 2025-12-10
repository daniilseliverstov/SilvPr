from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import LiveServerTestCase


class FunctionalTest(LiveServerTestCase):
    """
    Класс-родитель для всех функциональных тестов
    """

    def setUp(self):
        """
        Запускается перед каждым тестом.
        Открывает Браузер
        """
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 10)


    def tearDown(self):
        """Закрывает Браузер"""

        self.browser.quit()

    def go_to_homepage(self):
        """Переходит на главную страницу"""
        self.browser.get("http://localhost:8000")

    def find(self, locator):
        """Ждёт и возвращает элемент.

        Примеры:
            self.find((By.ID, "submit-button"))
            self.find((By.CLASS_NAME, "blogs-feed"))
            self.find((By.XPATH, "//h1[contains(text(), 'Лента')]")"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_text(self, text):
        """Находит текст на странице, для всплывающих окон или сообщений
        Примеры:
            self.wait_for_text("Пост успешно опубликован")
            self.wait_for_text("Вы вошли как admin")"""
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), text))

    def should_see(self, text):
        """
        Проверяет, что текст сейчас виден на странице.
        Пример:
            self.should_see("Лента блогов")
            """
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn(text, body_text, f"Ожидали увидеть текст: '{text}'")

    def should_see_in_title(self, text):
        """
        Проверяет, что текст есть в заголовке вкладки браузера.

        Примеры:
            self.should_see_in_title("Блоги - Главная")
            self.should_see_in_title("Админка")
        """
        self.assertIn(text, self.browser.title, f"Ожидали в title: '{text}'")
