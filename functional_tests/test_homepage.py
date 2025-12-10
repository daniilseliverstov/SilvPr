from .base import FunctionalTest
from selenium.webdriver.common.by import By


class HomePageTest(FunctionalTest):
    """Класс для проверки Главной страницы"""

    def test_home_page_look_correct(self):
        """Проверяет наличие основных элементов страницы"""
        self.go_to_homepage()

        self.should_see_in_title("The install worked successfully! Congratulations!")

        self.should_see("View release notes for Django 6.0")
        self.should_see("Tutorial: A Polling App")

