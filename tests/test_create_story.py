import unittest

import time

from browser import Browser


class TestCreateStory(unittest.TestCase):

    def setUp(self):
        self.driver = Browser()
        self.driver.goToFacebook()
        self.driver.login('taipeitechse@gmail.com', 'selab1623')

    def test_create_story(self):
        timestamp = str(time.time())
        self.driver.createStory('just for fun you know, i\'m testing all day long' + timestamp)
        time.sleep(5)
        assert self.driver.isStoryCreated('just for fun you know, i\'m testing all day long' + timestamp)

    def test_create_image_story(self):
        self.driver.uploadImageStory('../image.gif', 'uh.......')
        time.sleep(7)
        assert self.driver.isUploadedImageStory('SE TaipeiTech', 'uh.......')

    def test_create_video_story(self):
        self.driver.uploadVideoStory('../video.mp4', 'yap')

    def tearDown(self):
        self.driver.close()
