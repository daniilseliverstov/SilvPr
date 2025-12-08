from .base import FunctionalTest


class HomePageTest(FunctionalTest):
    """Класс для проверки Главной страницы"""

    def test_home_page_look_correct(self):
        """Проверяет наличие основных элементов страницы"""
        self.go_to_homepage()

        self.check_text_on_page("It worked!")
        self.check_text_on_page("Welcome to Django")


