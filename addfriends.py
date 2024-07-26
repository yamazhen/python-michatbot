import unittest
import time
from appium import webdriver
from appium.options.android.uiautomator2.skip_device_initialization_option import SkipDeviceInitializationOption
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

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)
        app_state = self.driver.query_app_state('com.michatapp.im')
        
        if app_state != 'RUNNING_IN_FOREGROUND':
            self.driver.activate_app('com.michatapp.im')

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def apprun(self,path,function,text=None,delay=0.5) -> None:
        try:
            el = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((AppiumBy.XPATH,path)))
            if function == 'click':
                element_text = el.text
                if element_text == 'Message':
                    notadd = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((AppiumBy.XPATH,'//android.widget.ImageButton[@content-desc="Navigate up"]')))
                    notadd.click()
                else:
                    el.click()
            if function == 'send_keys' and text:
                el.send_keys(text)
        except TimeoutException:
            print(f"Element not found for XPATH: {path}. Skipping")
    
    def ads(self):
        check_xpath = '//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View'
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((AppiumBy.XPATH, check_xpath)))
            print('Ads detected')
            time.sleep(30)
            self.apprun('//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View', 'click','Ads', 30)
        except TimeoutException:
            print('No Ads')

    def scroll_down(self):
        time.sleep(1)
        screen_size = self.driver.get_window_size()
        start_x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.9
        end_y = screen_size['height'] * 0.85 
        self.driver.swipe(start_x=start_x, start_y=start_y, end_x=start_x, end_y=end_y, duration=1000)
        
    def test_program(self) -> None:
        try:
            self.apprun('//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]', 'click')
            self.apprun('//android.widget.LinearLayout[@resource-id="com.michatapp.im:id/peopleNearby_item"]','click')
            index = 2
            while True:
                addlist_xpath = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.michatapp.im:id/peopleNearbyContent"]/android.widget.LinearLayout[{index}]'
                self.apprun(addlist_xpath, 'click')
                self.apprun('//android.widget.TextView[@resource-id="com.michatapp.im:id/action_textview"]', 'click')
                self.apprun('//android.widget.EditText[@resource-id="com.michatapp.im:id/request_information"]', 'send_keys', 'Hello!')
                self.apprun('//android.widget.TextView[@resource-id="com.michatapp.im:id/action_button"]', 'click')
                self.apprun('//android.widget.ImageButton[@content-desc="Navigate up"]', 'click')
                self.ads()
                index += 1
                self.scroll_down()

        except KeyboardInterrupt:
            print("Program stopped")

if __name__ == '__main__':
    unittest.main()
