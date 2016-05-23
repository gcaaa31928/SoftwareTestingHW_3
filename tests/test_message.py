import unittest

import time

from browser import Browser


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.driver = Browser()
        self.driver.goToFacebook()
        self.driver.login('taipeitechse@gmail.com', 'selab1623')

    def test_send_message(self):
        timestamp = str(time.time())
        self.driver.sendMessage('i am Mr.Big ' + str(timestamp))
        time.sleep(2)
        assert self.driver.isSendingMessage('i am Mr.Big ' + str(timestamp))

    def test_send_photo(self):
        timestamp = str(time.time())
        self.driver.sendPhotoMessage('image.gif')
        time.sleep(8)

    def tearDown(self):
        self.driver.close()
