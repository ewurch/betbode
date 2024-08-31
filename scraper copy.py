from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import os
from datetime import datetime, timedelta

HTML_FILE_PATH = 'html_cache/{url}.html'
CACHE_DURATION = timedelta(minutes=5)

def fetch_html_with_selenium(url):
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True  # Run in headless mode
    #service = Service('/opt/homebrew/Cellar/geckodriver')  # Update with the path to your WebDriver
    driver = webdriver.Firefox(options=options)
    
    # Load the page
    driver.get(url)
    
    # Wait for the JavaScript to load the content
    time.sleep(5)  # Adjust the sleep time as needed
    
    # Get the page source
    html_content = driver.page_source
    
    # Close the WebDriver
    driver.quit()
    
fetch_html_with_selenium('https://oddspedia.com/football/brazil/serie-a/odds')
