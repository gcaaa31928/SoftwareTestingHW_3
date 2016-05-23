#encoding=utf-8
import unittest

import time

from browser import Browser


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.driver = Browser()
        self.driver.goToFacebook()
        self.driver.login('taipeitechse@gmail.com', 'selab1623')
        time.sleep(2)
        self.driver.goToFacebookEvent()

    def test_create_event(self):
        timestamp = str(time.time())
        self.driver.createEvent('i will take 100 score ' + timestamp)
        time.sleep(2)
        assert self.driver.isCreatedEvent('i will take 100 score ' + timestamp)

    def test_invite_friends(self):
        timestamp = str(time.time())
        self.driver.createEvent('i will take 100 score ' + timestamp)
        time.sleep(4)
        self.driver.inviteFriend()
        time.sleep(2)
        self.driver.isInvitedFriend()

    def tearDown(self):
        self.driver.close()
