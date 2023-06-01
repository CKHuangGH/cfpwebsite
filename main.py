



import asyncio
from pyppeteer import launch

async def screenshot_full_page(url):
    # 啟動瀏覽器
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    # 取得網頁的完整高度
    height = await page.evaluate('() => document.documentElement.scrollHeight')

    # 設置瀏覽器視窗大小以容納整個頁面
    await page.setViewport({'width': 1920, 'height': height})

    # 生成長截圖
    screenshot = await page.screenshot()
    
    # 關閉瀏覽器
    await browser.close()

    return screenshot

# 執行截圖
url = 'https://www.sigapp.org/sac/sac2023/'
loop = asyncio.get_event_loop()
screenshot = loop.run_until_complete(screenshot_full_page(url))

# 儲存截圖
with open('screenshot.png', 'wb') as f:
    f.write(screenshot)



















# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import os
# import time
# import re
# from io import BytesIO
# from PIL import Image
 
 
# options = Options()
# options.add_argument("--disable-notifications")
 
# driver = webdriver.Chrome('./chromedriver', chrome_options=options)
# driver.get("https://2023.ieee-iscc.org/")
# time.sleep(2)

# # 取得頁面的高度
# scroll_height = driver.execute_script('return document.documentElement.scrollHeight')

# # 設置瀏覽器視窗大小以容納整個頁面
# driver.set_window_size(1920, scroll_height)

# # 等待視窗調整大小完成
# time.sleep(2)

# # 設定捲動步長
# scroll_step = 1000

# # 建立一個空白圖像物件，用於合併截圖
# screenshot = Image.new('RGB', (1920, scroll_height))

# # 捲動並進行截圖
# scroll_position = 0
# while scroll_position < scroll_height:
#     # 捲動到指定位置
#     driver.execute_script(f'window.scrollTo(0, {scroll_position});')
#     time.sleep(2)
    
#     # 截圖
#     screenshot_part = driver.get_screenshot_as_png()
#     screenshot_part = Image.open(BytesIO(screenshot_part))
    
#     # 將截圖合併到空白圖像中
#     screenshot.paste(screenshot_part, (0, scroll_position))
    
#     # 更新捲動位置
#     scroll_position += scroll_step
    
    
# # 儲存合併後的截圖
# screenshot.save('screenshot.png')

# # 關閉瀏覽器
# driver.quit()



























# # 取得頁面的高度
# scroll_height = driver.execute_script('return document.documentElement.scrollHeight')

# # 設置瀏覽器視窗大小以容納整個頁面
# driver.set_window_size(1920, scroll_height)

# # 等待視窗調整大小完成
# time.sleep(2)

# # 設定捲動步長
# scroll_step = 200

# # 計算捲動次數
# scroll_count = scroll_height // scroll_step

# # 建立一個空白圖像物件，用於合併截圖
# screenshot = Image.new('RGB', (1920, scroll_height))

# # 捲動並進行截圖
# for i in range(scroll_count):
#     # 捲動到指定位置
#     scroll_to = i * scroll_step
#     driver.execute_script(f'window.scrollTo(0, {scroll_to});')
#     time.sleep(2)
    
#     # 截圖
#     screenshot_part = driver.get_screenshot_as_png()
#     screenshot_part = Image.open(BytesIO(screenshot_part))
    
#     # 將截圖合併到空白圖像中
#     screenshot.paste(screenshot_part, (0, scroll_to))
    
# # 儲存合併後的截圖
# screenshot.save('screenshot.png')

# # 關閉瀏覽器
# driver.quit()