import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='ce12171c7da4911002',
    appPackage='com.michatapp.im',
    appActivity='com.michatapp.launch.LaunchActivity',
    noReset=True
)

appium_server_url = 'http://localhost:4723'

capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

message = 'Hello!'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)
        app_state = self.driver.query_app_state('com.michatapp.im')
        
        if app_state != 'RUNNING_IN_FOREGROUND':
            self.driver.activate_app('com.michatapp.im')

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def apprun(self,path,function,text=None,delay=1) -> None:
        try:
            el = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((AppiumBy.XPATH,path)))
            if function == 'send_keys' and text:
                el.send_keys(text)
                return
            method = getattr(el, function)
            method()
        except TimeoutException:
            print(f"Element not found for XPATH: {path}. Skipping")
    
    def ads(self):
        check_xpath = '//android.widget.FrameLayout[@content-desc="video-vd:09e568:0:2"]'
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((AppiumBy.XPATH, check_xpath)))
            print('Ads detected')
            time.sleep(40)
            self.apprun('//android.widget.ImageView[@content-desc="Ad closed"]', 'click')

        except TimeoutException:
            print('No Ads')

    def swipe_down(self):
        time.sleep(1)
        screen_size = self.driver.get_window_size()
        start_x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.9
        end_y = screen_size['height'] * 0.83
        self.driver.swipe(start_x=start_x, start_y=start_y, end_x=start_x, end_y=end_y, duration=1000)

    def test_program(self) -> None:
        try:
            self.apprun('//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]', 'click')
            self.apprun('//android.widget.LinearLayout[@resource-id="com.michatapp.im:id/peopleNearby_item"]','click')
            index = 1
            while True:
                profiles = f'(//android.widget.LinearLayout[@resource-id="com.michatapp.im:id/nb_item"])[1]'
                is_friends_xpath = f'{profiles}//android.widget.TextView[@resource-id="com.michatapp.im:id/is_friends"] | ' \
                   f'{profiles}//android.widget.TextView[@resource-id="com.michatapp.im:id/is_friends"][1] | ' \
                   f'{profiles}//android.widget.TextView[@resource-id="com.michatapp.im:id/is_friends"][2]'
                is_friends_elements = self.driver.find_elements(AppiumBy.XPATH, is_friends_xpath)

                if not is_friends_elements:
                    print('not friends')
                    self.apprun(profiles, 'click')
                    self.apprun('//android.widget.LinearLayout[@resource-id="com.michatapp.im:id/action_group"]', 'click')
                    self.apprun('//android.widget.EditText[@resource-id="com.michatapp.im:id/request_information"]', 'click')
                    self.apprun('//android.widget.EditText[@resource-id="com.michatapp.im:id/request_information"]', 'send_keys', message)
                    self.apprun('//android.widget.TextView[@resource-id="com.michatapp.im:id/action_button"]', 'click')
                    try:
                        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Profile"]')))
                        self.apprun('//android.widget.ImageButton[@content-desc="Navigate up"]', 'click')
                    except TimeoutException:
                        print('Profile not found')
                    #close ads for you (not needed if you have adblock)
                    #self.ads()
                    self.swipe_down()
                else:
                    print('friended')
                    self.swipe_down()
                index += 1

        except KeyboardInterrupt:
            print("Program stopped")

if __name__ == '__main__':
    unittest.main()
