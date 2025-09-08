import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class BaseInstallTest(unittest.TestCase):
    def setUp(self):  
        self.browser = webdriver.Firefox()  

    def tearDown(self):  
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("SilvPr", self.browser.title)

    def test_home_page_header(self):
        self.browser.get("http://localhost:8000")
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Сайт SilvPr", header_text)

    def test_home_page_blog(self):
        pass


if __name__ == "__main__":  
    unittest.main()  