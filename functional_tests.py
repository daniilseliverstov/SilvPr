import unittest
from selenium import webdriver


class BaseInstallTest(unittest.TestCase):
    def setUp(self):  
        self.browser = webdriver.Firefox()  

    def tearDown(self):  
        self.browser.quit()

    def test_install(self):

        self.browser.get("http://localhost:8000")  

        self.assertIn("Congratulations!", self.browser.title)



if __name__ == "__main__":  
    unittest.main()  