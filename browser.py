# !encoding=utf-8
import os
import traceback
from time import sleep
import time

from os.path import abspath
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def __init__(self, chrome=True):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        if chrome:
            self.device = webdriver.Chrome('G:\PATH\chromedriver.exe', chrome_options=chrome_options)
        else:
            self.device = webdriver.Firefox()

    def goToFacebook(self):
        self.device.get('http://www.facebook.com')
        assert 'Facebook' in self.device.title

    def goToFacebookEvent(self):
        self.device.get('https://www.facebook.com/events/upcoming?action_history=null')

    def goToFacebookPhotoManagement(self):
        self.device.get('https://www.facebook.com/se.taipeitech/allactivity?privacy_source=activity_log&log_filter=photos')

    def goToProfile(self):
        self.device.get('https://www.facebook.com/se.taipeitech')

    def login(self, account, password):
        try:
            element = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".menu_login_container"))
            )
            ele = self.device.find_element_by_id('email')
            ele.send_keys(account)
            ele = self.device.find_element_by_id('pass')
            ele.send_keys(password)
            button = self.device.find_element_by_id('u_0_w')
            button.click()
        except:
            traceback.print_exc()
            self.device.close()

    def isLogin(self):
        return len(self.device.find_elements_by_css_selector('#pagelet_welcome_box')) > 0

    def createStory(self, story):
        try:
            element = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@name='xhpc_message']"))
            )
            ele = self.device.find_element_by_xpath("//*[@name='xhpc_message']")
            ele.click()
            ele.send_keys(story)
            sleep(2)
            button = self.device.find_element_by_css_selector('#feedx_container button')
            button.click()

        except:
            traceback.print_exc()
            self.device.quit()

    def isStoryCreated(self, story):
        story_wrapper = self.device.find_elements_by_css_selector('.userContentWrapper')[0]
        actual_story = story_wrapper.find_element_by_css_selector('.userContent p').text
        return story in actual_story

    def uploadImageStory(self, file, story):
        try:
            elements = self.device.find_elements_by_xpath("//*[@name='xhpc_message']")
            if len(elements) > 0:
                elements[0].click()
                sleep(2)
            input_photo = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
            )
            image_path = abspath(file)
            print(image_path)
            input_photo.send_keys(image_path)
            input_content = self.device.find_element_by_xpath("//*[@id='feedx_container']//*[@role='combobox']")
            input_content.send_keys(story)
            send_button = WebDriverWait(self.device, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='react-composer-post-button']"))
            )
            send_button.click()
            sleep(2)

        except:
            traceback.print_exc()
            self.device.quit()

    def isUploadedImageStory(self, expected_name, story):
        story_wrapper = self.device.find_elements_by_css_selector('.userContentWrapper')[0]
        image_exists = len(story_wrapper.find_elements_by_css_selector('.uiScaledImageContainer')) > 0
        actual_story = story_wrapper.find_element_by_css_selector('.userContent p').text
        name = story_wrapper.find_element_by_css_selector('div > div >div > div> div span a').text
        return (story in actual_story) and image_exists and name == expected_name

    def uploadVideoStory(self, file, story):
        try:
            elements = self.device.find_elements_by_xpath("//*[@name='xhpc_message']")
            if len(elements) > 0:
                elements[0].click()
                sleep(2)
            input_photo = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
            )
            image_path = os.path.abspath('../image.gif')
            input_photo.send_keys(image_path)
            input_photo = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
            )
            image_path = os.path.abspath(file)
            input_photo.send_keys(image_path)
            send_button = WebDriverWait(self.device, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='react-composer-post-button']"))
            )
            send_button.click()
            wait_for_video_alert = WebDriverWait(self.device, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]'))
            )
            close_button = WebDriverWait(self.device, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.layerCancel'))
            )
            close_button.click()
        except:
            traceback.print_exc()
            # browser.quit()

    def postComments(self, content):
        try:
            offset = 50000
            for i in range(0, offset, 500):
                self.device.execute_script("window.scrollTo(0," + str(i) + ")")
                container = self.device.find_elements_by_css_selector('.userContentWrapper .UFIInputContainer')
                if len(container) > 0 and container[0].is_displayed():
                    container[0].click()
                    sleep(1)
                    input_composer = self.device.find_element_by_css_selector(
                        ".userContentWrapper .UFIInputContainer div[data-testid='ufi_comment_composer']")
                    input_composer.send_keys(content)
                    input_composer.send_keys(Keys.ENTER)
                    return
                sleep(1)
        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def isPostComments(self, content):
        offset = 50000
        for i in range(0, offset, 500):
            self.device.execute_script("window.scrollTo(0," + str(i) + ")")
            element = self.device.find_element_by_css_selector(' .UFICommentBody span')
            if content in element.text:
                return True
        return False

    def editComments(self, name, content):
        try:
            offset = 20000
            for i in range(0, offset, 400):
                self.device.execute_script("window.scrollTo(0," + str(i) + ")")
                comment_block = self.device.find_elements_by_css_selector('.UFICommentContentBlock')
                comments = self.device.find_elements_by_css_selector('.UFICommentContentBlock .UFICommentContent a')
                for comment in comments:
                    if comment.text == name and comment.is_displayed() and EC.element_to_be_clickable(comment):
                        hover = ActionChains(self.device).move_to_element(comment_block[0])
                        hover.perform()
                        sleep(1)
                        popup_button = self.device.find_element_by_css_selector('.UFICommentCloseButton')
                        popup_button.click()
                        sleep(1)
                        edit_ele = self.device.find_element_by_xpath('//*[@data-testid="ufi_comment_menu_edit"]')
                        edit_ele.click()
                        sleep(1)
                        input_comment = self.device.find_elements_by_xpath("//*[@data-testid='ufi_comment_composer']")[0]
                        input_comment.send_keys(content)
                        input_comment.send_keys(Keys.ENTER)
                        return
                sleep(1.5)
        except Exception, e:
            traceback.print_exc()
            self.device.quit()



    def deleteComments(self):
        try:
            comments = self.device.find_elements_by_css_selector('.UFICommentContentBlock .UFICommentContent a')
            hover = ActionChains(self.device).move_to_element(comments[0])
            hover.perform()
            sleep(1)
            popup_button = self.device.find_element_by_css_selector('.UFICommentCloseButton')
            popup_button.click()
            sleep(1)
            delete_ele = self.device.find_element_by_xpath('//*[@data-testid="ufi_comment_menu_delete"]')
            delete_ele.click()
            sleep(2)
            confirm_button = self.device.find_element_by_css_selector('.layerConfirm.uiOverlayButton')
            confirm_button.click()

        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def isDeletedComment(self):
        comment_blocks = self.device.find_elements_by_css_selector('.UFICommentContentBlock')
        return len(comment_blocks) == 0

    def likePosts(self):
        try:
            like_button = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="fb-ufi-likelink"]'))
            )
            like_button.click()
        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def unLikePosts(self):
        try:
            like_button = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="fb-ufi-unlikelink"]'))
            )
            like_button.click()
        except Exception, e:
            traceback.print_exc()
            self.device.quit()


    def isLikePosts(self, user):
        like_html_block = self.device.find_elements_by_css_selector('.UFIRow.UFILikeSentence')
        if len(like_html_block) == 0:
            return False
        html = like_html_block[0].get_attribute('innerHTML')
        return user in html


    def sendMessage(self, content):
        try:
            chat_button = self.device.find_element_by_css_selector('#fbDockChatBuddylistNub .fbNubButton')
            if chat_button.is_displayed():
                chat_button.click()
            chat_list = WebDriverWait(self.device, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbChatOrderedList ul li'))
            )
            chat_list.click()
            chat_block = WebDriverWait(self.device, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbNubFlyoutFooter div[role="textbox"]'))
            )
            chat_block.click()
            chat_block.send_keys(content)
            chat_block.send_keys(Keys.ENTER)

        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def isSendingMessage(self, content):
        conversation = self.device.find_element_by_css_selector('.conversation').get_attribute('innerHTML')
        return content in conversation

    def sendPhotoMessage(self, photo_url):
        try:
            chat_button = self.device.find_element_by_css_selector('#fbDockChatBuddylistNub .fbNubButton')
            if chat_button.is_displayed():
                chat_button.click()
            chat_list = WebDriverWait(self.device, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbChatOrderedList ul li'))
            )
            chat_list.click()
            sleep(2)


            chat_block = WebDriverWait(self.device, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fbNubFlyoutFooter div[role="textbox"]'))
            )
            chat_block.click()
            sleep(1)
            input_location = "//div[@class='fbNubFlyoutFooter']/div/div[2]/form/div/input[@type='file']"
            script = "document.evaluate(\""+input_location+"\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
            self.device.execute_script(script=script)
            sleep(2)
            attachment = self.device.find_element_by_xpath('//*[@name="attachment[]"]')
            # browser.find_element_by_name('attachment[]').click(
            image_path = os.path.abspath(photo_url)
            print image_path
            attachment.send_keys(image_path)
        except Exception, e:
            traceback.print_exc()
            # browser.quit()



    def createEvent(self, title):
        try:
            create_event = WebDriverWait(self.device, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="event-create-button"]'))
            )
            create_event.click()
            event_name = WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.uiLayer div[role="dialog"] input[type="text"]'))
            )
            event_name.send_keys(title)
            confirm_button = self.device.find_element_by_css_selector('button.layerConfirm')
            confirm_button.click()

        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def isCreatedEvent(self, title):
        try:
            event_list = self.device.find_element_by_css_selector('#event_header_info').get_attribute('innerHTML')
            return title in event_list
        except Exception, e:
            traceback.print_exc()
            self.device.quit()


    def inviteFriend(self):
        try:
            invited_button = self.device.find_element_by_css_selector('#event_button_bar .fbEventClassicButton')
            invited_button.click()
            WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.uiScrollableArea .uiGrid'))
            )
            invited_people = self.device.find_elements_by_css_selector('.uiScrollableArea .uiGrid')
            for person in invited_people:
                person.click()
                sleep(0.2)
            sleep(1)
            confirm_button = self.device.find_element_by_css_selector('.layerConfirm.uiOverlayButton')
            confirm_button.click()
        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def isInvitedFriend(self):
        try:
            invited_dialog = self.device.find_element_by_css_selector('td.vTop:nth-child(3) a')
            invited_dialog.click()
            WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.className a'))
            )
            area =  self.device.find_elements_by_css_selector('.uiScrollableAreaContent > *')
            return len(area) > 1

        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def deletePhotos(self):
        try:
            manage_button = WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[data-tooltip-content="允許發佈在動態時報"]'))
            )
            manage_button.click()
            sleep(2)
            delete_button = self.device.find_element_by_css_selector('li.__MenuItem:nth-child(4) > a:nth-child(1)')
            delete_button.click()
            confirm_button = WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.layerConfirm.uiOverlayButton'))
            )
            confirm_button.click()
        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def sharePost(self, content):
        try:
            share_button = WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.share_action_link'))
            )
            share_button.click()
            sleep(2)
            share_post_button = WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.uiLayer:not(.hidden_elem) .__MenuItem:nth-child(2)'))
            )
            share_post_button.click()
            input_content = WebDriverWait(self.device, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.uiLayer:not(.hidden_elem) div[contenteditable="true"]'))
            )
            input_content.send_keys(content)
            post_button = self.device.find_element_by_css_selector('.uiLayer:not(.hidden_elem) button:nth-child(2)')
            post_button.click()
            sleep(2)
            click = ActionChains(self.device).click()
            click.perform()
            # self.device.find_element_by_css_selector('div').click()
        except Exception, e:
            traceback.print_exc()
            self.device.quit()

    def close(self):
        self.device.close()

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
