from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import re

 
 
options = Options()
options.add_argument("--disable-notifications")
 
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://2023.ieee-iscc.org/")
chrome.get_screenshot_as_file("2330.png")

soup = BeautifulSoup(chrome.page_source, 'html.parser')

#print(soup.prettify())

print(soup.find_all(string=re.compile("^2023")))
os.system("pause")