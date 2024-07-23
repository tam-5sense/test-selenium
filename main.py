
import time
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

REQUIREMENTS_ITEMS = ['Access Tokens', 'Business Roles', 'Instagram Shop']
EXAMPLE_JSON = {
    "Access Tokens": {
        "class_name": "access",
        "text": "User"
    },
    "Business Roles": {
        "class_name": "business",
        "text": "User"
    },
    "Instagram Shop": {
        "class_name": "instagram",
        "text": "User"
    }
}
class Chrome:
    def headless_lambda(self, device, isAddOption=True):
        options = webdriver.ChromeOptions()
        if (device == 'PC'):
            print("pc")
            options.add_argument(f"--window-size={1920}x{1080}")
        else:
            # options.add_argument("--auto-open-devtools-for-tabs")
            options.add_argument(f"--window-size={640}x{1024}")
            mobile_emulation = {
                "deviceMetrics": {"width": 640, "height": 1024, "pixelRatio": 1.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
            options.add_experimental_option(
                "mobileEmulation", mobile_emulation)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--single-process")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(
            f"--user-agent=Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36")

        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(
        # ), options=options) if isAddOption else webdriver.Chrome(executable_path=ChromeDriverManager().install())

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) if isAddOption else webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        (driver.page_source).encode('utf-8')

        driver.maximize_window()

        return driver


def main():
    chrome = Chrome()
    driver = chrome.headless_lambda(device="PC", isAddOption=True)

    try:
        driver.get("https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user?locale=en_US")
        time.sleep(5)
        print('Page loaded')
        # get element of class name is row_3 _5m29
        element = driver.find_element(By.CLASS_NAME, 'row_3')
        print('Element found')
        print(element.text)
        driver.implicitly_wait(10)
        driver.save_screenshot('screenshot.png')
        print('Screenshot saved')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()

