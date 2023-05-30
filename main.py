from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
 
 
options = Options()
options.add_argument("--disable-notifications")  # 取消所有的alert彈出視窗
 
browser = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=options)
 
browser.get("https://2023.ieee-iscc.org/")
    
 # 定位搜尋框
element=browser.find_element_by_class_name("gLFyf.gsfi")
# 傳入字串
element.send_keys("Selenium Python")
#soup = BeautifulSoup(browser.page_source, "html.parser")