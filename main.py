
import time
import os
import json
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
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

        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) if isAddOption else webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # (driver.page_source).encode('utf-8')

        # driver.maximize_window()
        
         # Create a Service object with the specified path
        service = ChromeService(executable_path=CHROMEDRIVER_PATH)
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver


def clean_html(html_content):
    """Clean HTML content and extract text."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def process_selectors(driver, selectors):
    """Process a list of selectors and extract data from elements."""
    texts = []

    if isinstance(selectors, str):
        selectors = [selectors]

    # Regular expressions for tag#id and #id patterns
    tag_id_pattern = re.compile(r'^([a-zA-Z0-9]+)#(\w+)$')
    id_pattern = re.compile(r'^#(\w+)$')

    for selector in selectors:
        try:
            # Check if selector matches tag#id pattern
            match_tag_id = tag_id_pattern.match(selector)
            if match_tag_id:
                tag, _id = match_tag_id.groups()
                css_selector = f"{tag}#{_id}"  # Construct CSS selector
                print(f"Processing tag#id selector: {css_selector}")
                
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                    )
                    html_content = element.get_attribute('innerHTML').strip()
                    text_content = clean_html(html_content)
                    print(f"Extracted text from element: {text_content}")
                    texts.append(text_content)
                except TimeoutException:
                    print(f"Timeout waiting for tag#id selector: {css_selector}")
                    texts.append(f"Timeout waiting for tag#id selector: {css_selector}")
                except NoSuchElementException:
                    print(f"No such element for tag#id selector: {css_selector}")
                    texts.append(f"No such element for tag#id selector: {css_selector}")
                except WebDriverException as e:
                    print(f"WebDriver exception for tag#id selector: {css_selector}: {str(e)}")
                    texts.append(f"WebDriver exception for tag#id selector: {css_selector}: {str(e)}")

            # Check if selector matches #id pattern
            elif id_pattern.match(selector):
                _id = selector.lstrip('#')
                css_selector = f"#{_id}"  # Construct CSS selector
                print(f"Processing ID selector: {css_selector}")
                
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                    )
                    html_content = element.get_attribute('innerHTML').strip()
                    text_content = clean_html(html_content)
                    print(f"Extracted text from element: {text_content}")
                    texts.append(text_content)
                except TimeoutException:
                    print(f"Timeout waiting for ID selector: {css_selector}")
                    texts.append(f"Timeout waiting for ID selector: {css_selector}")
                except NoSuchElementException:
                    print(f"No such element for ID selector: {css_selector}")
                    texts.append(f"No such element for ID selector: {css_selector}")
                except WebDriverException as e:
                    print(f"WebDriver exception for ID selector: {css_selector}: {str(e)}")
                    texts.append(f"WebDriver exception for ID selector: {css_selector}: {str(e)}")

            else:
                # Handle other CSS selectors (like class or attribute selectors)
                print(f"Processing general CSS selector: {selector}")
                try:
                    elements = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                    if not elements:
                        print(f"No elements found for CSS selector: {selector}")
                        texts.append(f"No elements found for CSS selector: {selector}")
                    for element in elements:
                        html_content = element.get_attribute('innerHTML').strip()
                        text_content = clean_html(html_content)
                        print(f"Extracted text from element: {text_content}")
                        texts.append(text_content)
                except TimeoutException:
                    print(f"Timeout waiting for CSS selector: {selector}")
                    texts.append(f"Timeout waiting for CSS selector: {selector}")
                except NoSuchElementException:
                    print(f"No such elements for CSS selector: {selector}")
                    texts.append(f"No such elements for CSS selector: {selector}")
                except WebDriverException as e:
                    print(f"WebDriver exception for CSS selector: {selector}: {str(e)}")
                    texts.append(f"WebDriver exception for CSS selector: {selector}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error for selector '{selector}': {str(e)}")
            texts.append(f"Unexpected error for selector '{selector}': {str(e)}")

    return texts

def extract_data(driver, selector_mapping):
    """Extract data based on the selector mapping."""
    extracted_data = {}

    if not isinstance(selector_mapping, dict):
        raise ValueError("selector_mapping should be a dictionary.")

    print(f"Processing selector mapping: {selector_mapping}")

    for item_key, item_details in selector_mapping.items():
        if isinstance(item_details, dict):
            selectors = item_details.get("selectors") or item_details.get("selector", [])
            if isinstance(selectors, str):
                selectors = [selectors]

            print(f"Processing selectors for {item_key}: {selectors}")
            item_data = {
                "selectors": selectors,
                "texts": process_selectors(driver, selectors)
            }
            
            # Process nested selectors
            for sub_key, sub_details in item_details.items():
                if isinstance(sub_details, dict) and sub_key not in ["selector", "selectors"]:
                    print(f"Processing nested selectors for {item_key} -> {sub_key}: {sub_details}")
                    item_data[sub_key] = extract_data(driver, sub_details)

            extracted_data[item_key] = item_data

    return extracted_data

def scan_url(driver, url, selector_mapping, output_file):
    """Scan the URL and save extracted data to a file."""
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    print(f'Page loaded: {url}')
    print(f"Selector Mapping: {selector_mapping}")

    if not isinstance(selector_mapping, dict):
        raise ValueError(f"selector_mapping should be a dictionary, got {type(selector_mapping)}")

    data = extract_data(driver, selector_mapping)
    formatted_data = json.dumps(data, indent=4)
    print('Data extracted:')
    print(formatted_data)

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Data saved to {output_file}')

def main():
    """Main function to set up and run the Selenium WebDriver."""
    chrome = Chrome()
    driver = chrome.headless_lambda(device="PC", isAddOption=True)
    
    try:
        try:
            with open('config.json', 'r') as f:
                url_config = json.load(f)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please ensure that 'config.json' exists in the correct directory.")
            return
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

        print(f"Raw JSON content: {url_config}")

        for config in url_config:
            selectors = config.get("selectors")
            if not isinstance(selectors, dict):
                raise ValueError("Expected 'selectors' to be a dictionary.")
            
            scan_url(driver, config["url"], selectors, config["output_file"])
    finally:
        driver.quit()

if __name__ == '__main__':
    main()