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


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome('G:\PATH\chromedriver.exe', chrome_options=chrome_options)

def GoToFacebook():
    browser.get('http://www.facebook.com')
    assert 'Facebook' in browser.title

def Login(account, password):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".menu_login_container"))
        )
        ele = browser.find_element_by_id('email')
        ele.send_keys(account)
        ele = browser.find_element_by_id('pass')
        ele.send_keys(password)
        button = browser.find_element_by_id('u_0_w')
        button.click()
        sleep(2)
        assert len(browser.find_elements_by_css_selector('#pagelet_welcome_box')) > 0
    except :
        print '12'
        browser.quit()

def CreateStory(story):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@name='xhpc_message']"))
        )
        ele = browser.find_element_by_xpath("//*[@name='xhpc_message']")
        ele.click()
        ele.send_keys(story)
        sleep(2)
        button = browser.find_element_by_css_selector('#feedx_container button')
        button.click()
        sleep(5)
        story_wrapper = browser.find_elements_by_css_selector('.userContentWrapper')[0]
        actual_story = story_wrapper.find_element_by_css_selector('.userContent p').text
        assert story in actual_story
    except :
        print '12'
        browser.quit()

def UploadImageStory(file, story):
    try:
        elements = browser.find_elements_by_xpath("//*[@name='xhpc_message']")
        if len(elements) > 0:
            elements[0].click()
            sleep(2)
        input_photo = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
        )
        image_path = os.path.abspath(file)
        input_photo.send_keys(image_path)
        input_content = browser.find_element_by_xpath("//*[@id='feedx_container']//*[@role='combobox']")
        input_content.send_keys(story)
        send_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='react-composer-post-button']"))
        )
        send_button.click()
        sleep(2)
        story_wrapper = browser.find_elements_by_css_selector('.userContentWrapper')[0]
        assert len(story_wrapper.find_elements_by_css_selector('.uiScaledImageContainer')) > 0
        actual_story = story_wrapper.find_element_by_css_selector('.userContent p').text
        assert story in actual_story
    except :
        traceback.print_exc()
        browser.quit()

def UploadVideoStory(file, story):
    try:
        elements = browser.find_elements_by_xpath("//*[@name='xhpc_message']")
        if len(elements) > 0:
            elements[0].click()
            sleep(2)
        input_photo = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
        )
        image_path = os.path.abspath('image.gif')
        input_photo.send_keys(image_path)
        input_photo = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='feedx_container']//*[@name='composer_photo[]']"))
        )
        image_path = os.path.abspath(file)
        input_photo.send_keys(image_path)
        send_button = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='react-composer-post-button']"))
        )
        send_button.click()
        wait_for_video_alert = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]'))
        )
        close_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.layerCancel'))
        )
        close_button.click()
    except :
        traceback.print_exc()
        # browser.quit()

def PostComments(content):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.UFIInputContainer'))
        )
        element.click()
        sleep(1)
        element = browser.find_elements_by_xpath("//*[@data-testid='ufi_comment_composer']")[0]
        element.send_keys(content)
        element.send_keys(Keys.ENTER)
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentBody span'))
        )
        assert content in element.text
        # ele.send_keys("G:/Projects/SoftwareTestingHW#/image.gif")
        # ele = browser.find_element_by_xpath("//*[@name='composer_photo[]']")

    except Exception, e:
        traceback.print_exc()
        browser.quit()

def EditComments(content):
    try:
        comment_block = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentContentBlock'))
        )
        hover = ActionChains(browser).move_to_element(comment_block)
        hover.perform()
        sleep(1)
        popup_button = browser.find_element_by_css_selector('.UFICommentCloseButton')
        popup_button.click()
        sleep(1)
        edit_ele = browser.find_element_by_xpath('//*[@data-testid="ufi_comment_menu_edit"]')
        edit_ele.click()
        input_comment = browser.find_elements_by_xpath("//*[@data-testid='ufi_comment_composer']")[0]
        input_comment.send_keys(content)
        input_comment.send_keys(Keys.ENTER)
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentBody span'))
        )
        assert content in element.text
    except Exception, e:
        traceback.print_exc()
        browser.quit()

def DeleteComments():
    try:
        comment_block = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.UFICommentContentBlock'))
        )
        hover = ActionChains(browser).move_to_element(comment_block)
        hover.perform()
        sleep(1)
        popup_button = browser.find_element_by_css_selector('.UFICommentCloseButton')
        popup_button.click()
        sleep(1)
        edit_ele = browser.find_element_by_xpath('//*[@data-testid="ufi_comment_menu_delete"]')
        edit_ele.click()
        sleep(2)
        confirm_button = browser.find_element_by_css_selector('.layerConfirm.uiOverlayButton')
        confirm_button.click()
        comment_blocks = browser.find_elements_by_css_selector('.UFICommentContentBlock')
        assert len(comment_blocks) == 0
    except Exception, e:
        traceback.print_exc()
        browser.quit()

def LikePosts():
    try:
        like_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="fb-ufi-likelink"]'))
        )
        like_button.click()

    except Exception, e:
        traceback.print_exc()
        browser.quit()


GoToFacebook()
Login('taipeitechse@gmail.com', 'selab1623')
CreateStory('tested for cliu ya selab !!' + str(time.time()))
LikePosts()
# UploadImageStory('image.gif', 'yap, suck you know')
# UploadVideoStory('video.mp4', 'yap, suck you know')
# PostComments('hell')
# EditComments('hell god editting')
# DeleteComments()
