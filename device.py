# !encoding=utf-8
import os
import traceback
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Device():

    def __init__(self, chrome=True):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        if chrome:
            self.browser = webdriver.Chrome('G:\Work\PATH\chromedriver.exe', chrome_options=chrome_options)
        else:
            self.browser = webdriver.Firefox()

    def GoToFacebook(self):
        self.browser.get('http://www.facebook.com')
        assert 'Facebook' in self.browser.title

    def Login(self, account, password):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".menu_login_container"))
            )
            ele = self.browser.find_element_by_id('email')
            ele.send_keys(account)
            ele = self.browser.find_element_by_id('pass')
            ele.send_keys(password)
            button = self.browser.find_element_by_id('u_0_w')
            button.click()
        except :
            traceback.print_exc()
            self.browser.close()

    def IsLogin(self):
        return len(self.browser.find_elements_by_css_selector('#pagelet_welcome_box')) > 0

    def CreateStory(self, story):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@name='xhpc_message']"))
            )
            ele = self.browser.find_element_by_xpath("//*[@name='xhpc_message']")
            ele.click()
            ele.send_keys(story)
            sleep(2)
            button = self.browser.find_element_by_css_selector('#feedx_container button')
            button.click()

        except :
            traceback.print_exc()
            self.browser.quit()

    def IsStoryCreated(self, story):
        story_wrapper = self.browser.find_elements_by_css_selector('.userContentWrapper')[0]
        actual_story = story_wrapper.find_element_by_css_selector('.userContent p').text
        return story in actual_story

    def UploadImageStory(self, file, story):
        try:
            elements = self.browser.find_elements_by_xpath("//*[@name='xhpc_message']")
            if len(elements) > 0:
                elements[0].click()
                sleep(2)
            input_photo = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
            )
            image_path = os.path.abspath(file)
            input_photo.send_keys(image_path)
            input_content = self.browser.find_element_by_xpath("//*[@id='feedx_container']//*[@role='combobox']")
            input_content.send_keys(story)
            send_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='react-composer-post-button']"))
            )
            send_button.click()
            sleep(2)

        except :
            traceback.print_exc()
            self.browser.quit()

    def IsUploadedImageStory(self, name, file, story):
        story_wrapper = self.browser.find_elements_by_css_selector('.userContentWrapper')[0]
        image_exists = len(story_wrapper.find_elements_by_css_selector('.uiScaledImageContainer')) > 0
        actual_story = story_wrapper.find_element_by_css_selector('.userContent p').text
        expected_name = story_wrapper.find_element_by_css_selector('div > div >div > div> div span a').text
        return (story in actual_story) and image_exists and name == expected_name

    def UploadVideoStory(self, file, story):
        try:
            elements = self.browser.find_elements_by_xpath("//*[@name='xhpc_message']")
            if len(elements) > 0:
                elements[0].click()
                sleep(2)
            input_photo = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
            )
            image_path = os.path.abspath('image.gif')
            input_photo.send_keys(image_path)
            input_photo = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
            )
            image_path = os.path.abspath(file)
            input_photo.send_keys(image_path)
            send_button = WebDriverWait(self.browser, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='react-composer-post-button']"))
            )
            send_button.click()
            wait_for_video_alert = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]'))
            )
            close_button = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.layerCancel'))
            )
            close_button.click()
        except :
            traceback.print_exc()
            # browser.quit()

    def PostComments(self, content):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.UFIInputContainer'))
            )
            element.click()
            sleep(1)
            element = self.browser.find_elements_by_xpath("//*[@data-testid='ufi_comment_composer']")[0]
            element.send_keys(content)
            element.send_keys(Keys.ENTER)
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentBody span'))
            )
            assert content in element.text
            # ele.send_keys("G:/Projects/SoftwareTestingHW#/image.gif")
            # ele = browser.find_element_by_xpath("//*[@name='composer_photo[]']")

        except Exception, e:
            traceback.print_exc()
            self.browser.quit()

    def EditComments(self, content):
        try:
            comment_block = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentContentBlock'))
            )
            hover = ActionChains(self.browser).move_to_element(comment_block)
            hover.perform()
            sleep(1)
            popup_button = self.browser.find_element_by_css_selector('.UFICommentCloseButton')
            popup_button.click()
            sleep(1)
            edit_ele = self.browser.find_element_by_xpath('//*[@data-testid="ufi_comment_menu_edit"]')
            edit_ele.click()
            input_comment = browser.find_elements_by_xpath("//*[@data-testid='ufi_comment_composer']")[0]
            input_comment.send_keys(content)
            input_comment.send_keys(Keys.ENTER)
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentBody span'))
            )
            assert content in element.text
        except Exception, e:
            traceback.print_exc()
            self.browser.quit()

    def DeleteComments(self):
        try:
            comment_block = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentContentBlock'))
            )
            hover = ActionChains(self.browser).move_to_element(comment_block)
            hover.perform()
            sleep(1)
            popup_button = self.browser.find_element_by_css_selector('.UFICommentCloseButton')
            popup_button.click()
            sleep(1)
            edit_ele = self.browser.find_element_by_xpath('//*[@data-testid="ufi_comment_menu_delete"]')
            edit_ele.click()
            sleep(2)
            confirm_button = self.browser.find_element_by_css_selector('.layerConfirm.uiOverlayButton')
            confirm_button.click()
            comment_blocks = browser.find_elements_by_css_selector('.UFICommentContentBlock')
            assert len(comment_blocks) == 0
        except Exception, e:
            traceback.print_exc()
            self.browser.quit()

    def LikePosts(self, user):
        try:
            like_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="fb-ufi-likelink"]'))
            )
            like_button.click()
            like_html_block = self.browser.find_element_by_css_selector('.UFIRow').get_attribute('innerHTML')
            assert user in like_html_block

        except Exception, e:
            traceback.print_exc()
            self.browser.quit()

    def SendMessage(self, content):
        try:
            chat_button = self.browser.find_element_by_css_selector('#fbDockChatBuddylistNub .fbNubButton')
            if chat_button.is_displayed():
                chat_button.click()
            chat_list = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbChatOrderedList ul li'))
            )
            chat_list.click()
            chat_block = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbNubFlyoutFooter div[role="textbox"]'))
            )
            chat_block.click()
            chat_block.send_keys(content)
            chat_block.send_keys(Keys.ENTER)
            conversation = self.browser.find_element_by_css_selector('.conversation').get_attribute('innerHTML')
            assert content in conversation
        except Exception, e:
            traceback.print_exc()
            self.browser.quit()

    def SendPhotoMessage(self, photo_url):
        try:
            chat_button = self.browser.find_element_by_css_selector('#fbDockChatBuddylistNub .fbNubButton')
            if chat_button.is_displayed():
                chat_button.click()
            chat_list = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbChatOrderedList ul li'))
            )
            chat_list.click()
            chat_block = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbNubFlyoutFooter div[role="textbox"]'))
            )
            chat_block.click()
            # sleep(1)
            # clicked_attachment = browser.find_element_by_css_selector('form[title="加新相片"] div')
            # clicked_attachment.click()
            # attachment = WebDriverWait(browser, 5).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="attachment[]"]'))
            # )
            sleep(2)
            attachment = self.browser.find_element_by_xpath('//*[@name="attachment[]"]')
            # browser.find_element_by_name('attachment[]').click(
            # browser.find_element_by_css_selector('input.hidde)
            image_path = os.path.abspath(photo_url)
            print image_path
            attachment.clear()
            attachment.send_keys("G:\\Game\\SoftwareTestingHW_3\\image.gif")
        except Exception, e:
            traceback.print_exc()
            # browser.quit()

# GoToFacebook()
# Login('taipeitechse@gmail.com', 'selab1623')
# CreateStory('tested for cliu ya selab !!' + str(time.time()))
# LikePosts('SE TaipeiTech')
# UploadImageStory('image.gif', 'yap, suck you know')
# UploadVideoStory('video.mp4', 'yap, suck you know')
# PostComments('hell')
# EditComments('hell god editting')
# DeleteComments()
# SendPhotoMessage('image.gif')
