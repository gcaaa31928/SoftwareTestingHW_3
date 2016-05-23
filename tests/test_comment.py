import unittest

import time

from browser import Browser


class TestComment(unittest.TestCase):

    def setUp(self):
        self.driver = Browser()
        self.driver.goToFacebook()
        self.driver.login('taipeitechse@gmail.com', 'selab1623')
        self.driver.createStory('cliu is good' + str(time.time()))
        time.sleep(5)

    def test_like(self):
        self.driver.likePosts()
        time.sleep(3)
        assert self.driver.isLikePosts('SE TaipeiTech')

    def test_unlike(self):
        self.driver.likePosts()
        time.sleep(2)
        self.driver.unLikePosts()
        time.sleep(2)
        assert not self.driver.isLikePosts('SE TaipeiTech')

    def test_share(self):
        timestamp = time.time()
        self.driver.sharePost('ya, just share it ' + str(timestamp))
        self.driver.goToProfile()
        time.sleep(3)
        assert self.driver.isStoryCreated('ya, just share it ' + str(timestamp))

    def tearDown(self):
        self.driver.close()
