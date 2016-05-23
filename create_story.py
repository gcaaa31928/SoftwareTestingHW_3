from selenium import webdriver


class CreateStory():

    def setUP(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome('G:\Work\PATH\chromedriver.exe', chrome_options=chrome_options)

