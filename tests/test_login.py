import unittest

from browser import Browser


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = Browser()
        self.driver.goToFacebook()

    def test_login(self):
        self.driver.login('taipeitechse@gmail.com', 'selab1623')
        assert self.driver.isLogin()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
