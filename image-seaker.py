import os, re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import requests
# Set the path to the Chrome WebDriver executable
webdriver_path = 'D:\Finance\Finance_project\chromedriver'

# Create a Chrome WebDriver instance
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode, without opening a browser window
driver = webdriver.Chrome(executable_path=webdriver_path) # , options=chrome_options

# URL of the home page
url = 'https://cryptologos.cc/'

# Load the page with Selenium
driver.get(url)

# Wait for the dynamic content to load (you might need to adjust the waiting time based on the page's loading speed)
time.sleep(3)

# Create a directory to save the downloaded images
directory = 'cryptologos-svg'
os.makedirs(directory, exist_ok=True)

# Find all the image elements on the page
image_elements = driver.find_elements(By.TAG_NAME, "img")

# Download each image
for img_element in image_elements:
    # img_url = img_element.get_attribute('src')
    img_alt = img_element.get_attribute('alt')
    img_name = re.search("\((.*)\)", img_alt).group(1)
    img_file_name = img_alt.lower().replace('(', '').replace(')','').replace(' thumb', '').replace(' ','-')
    img_url = f'https://cryptologos.cc/logos/{img_file_name}.svg?v=025'
    print(img_url)
    print(img_name)
    # img_name = img_url.split('/')[-1]
    # img_path = os.path.join(directory, img_name)
    img_path = os.path.join(directory, img_name+'.svg')
    try:
        # Use the requests library to download the image
        response = requests.get(img_url)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)
        print(f"Downloaded: {img_alt}")
    except Exception as e:
        print(f"Failed to download: {img_alt}\nError: {str(e)}")

# Quit the WebDriver
driver.quit()
