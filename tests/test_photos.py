import unittest

import time

from browser import Browser


class TestPhoto(unittest.TestCase):

    def setUp(self):
        self.driver = Browser()
        self.driver.goToFacebook()
        self.driver.login('taipeitechse@gmail.com', 'selab1623')
        time.sleep(2)
        self.driver.goToFacebookPhotoManagement()
        time.sleep(3)

    def test_delete_photo(self):
        self.driver.deletePhotos()
        time.sleep(3)


    def tearDown(self):
        self.driver.close()
