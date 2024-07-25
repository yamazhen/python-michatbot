import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='emulator-5554',
    appPackage='com.michatapp.im',
    appActivity='com.michatapp.launch.LaunchActivity',
)

appium_server_url = 'http://localhost:4723'

capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_click_element(self) -> None:
        self.driver.implicitly_wait(5)
        start1_xpath = '//android.widget.TextView[@resource-id="com.michatapp.im:id/md_buttonDefaultPositive"]'
        start1 = self.driver.find_element(by=AppiumBy.XPATH, value=start1_xpath)
        start1.click()
        self.driver.implicitly_wait(5)

        start2_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
        start2 = self.driver.find_element(by=AppiumBy.XPATH, value=start2_xpath)
        start2.click()
        self.driver.implicitly_wait(5)
        start2.click()
        self.driver.implicitly_wait(5)

        el1_xpath = '//android.widget.TextView[@text="Log in with Google"]'
        el1 = self.driver.find_element(by=AppiumBy.XPATH, value=el1_xpath)
        el1.click()
        self.driver.implicitly_wait(5)

        el2_xpath = '(//android.widget.LinearLayout[@resource-id="com.google.android.gms:id/container"])[2]/android.widget.LinearLayout'
        el2 = self.driver.find_element(by=AppiumBy.XPATH, value=el2_xpath)
        el2.click()
        self.driver.implicitly_wait(5)

        el3_xpath = '//android.widget.EditText[@resource-id="com.michatapp.im:id/phone_number_input"]'
        el3 = self.driver.find_element(by=AppiumBy.XPATH, value=el3_xpath)
        el3.clear()
        el3.send_keys('0137413362')
        self.driver.implicitly_wait(5)

        el4_xpath = '//android.widget.TextView[@resource-id="com.michatapp.im:id/mobile_number_call_code"]'
        el4 = self.driver.find_element(by=AppiumBy.XPATH, value=el4_xpath)
        el4.click()
        self.driver.implicitly_wait(40)

if __name__ == '__main__':
    unittest.main()
