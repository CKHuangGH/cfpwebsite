import asyncio
from pyppeteer import launch
from cnocr import CnOcr

from selenium import webdriver
from PIL import Image

def capture_long_website_screenshot(url):
    # Set up the Selenium webdriver
    driver = webdriver.Chrome()  # Change to the appropriate driver for your browser
    driver.get(url)

    # Get the total height of the webpage
    total_height = driver.execute_script("return document.documentElement.scrollHeight")

    # Set the viewport dimensions
    viewport_width = driver.execute_script("return document.documentElement.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Calculate the number of scrolls needed
    num_scrolls = (total_height // viewport_height) + 1

    # Create a new image to store the long screenshot
    image = Image.new('RGB', (viewport_width, total_height))

    # Capture and stitch screenshots while scrolling the webpage
    scroll_height = 0
    for _ in range(num_scrolls):
        driver.save_screenshot("screenshot.png")

        screenshot = Image.open("screenshot.png")
        image.paste(screenshot, (0, scroll_height))

        driver.execute_script(f"window.scrollTo(0, {scroll_height + viewport_height})")
        scroll_height += viewport_height

    # Crop the image to the exact height of the webpage
    image = image.crop((0, 0, viewport_width, total_height))

    # Save the final long screenshot
    image.save('long_website_screenshot.png')

    # Close the web driver
    driver.quit()

# Call the function and provide the URL of the website you want to capture
url = "https://www.example.com"
capture_long_website_screenshot(url)














# async def screenshot_full_page(url):
#     # 啟動瀏覽器
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto(url)

#     # 取得網頁的完整高度
#     height = await page.evaluate('() => document.documentElement.scrollHeight')

#     # 設置瀏覽器視窗大小以容納整個頁面
#     await page.setViewport({'width': 1920, 'height': height})

#     # 生成長截圖
#     screenshot = await page.screenshot()
    
#     # 關閉瀏覽器
#     await browser.close()

#     return screenshot

# # 執行截圖
# url = 'https://2023.ieee-iscc.org/'
# loop = asyncio.get_event_loop()
# screenshot = loop.run_until_complete(screenshot_full_page(url))

# # 儲存截圖
# with open('screenshot.png', 'wb') as f:
#     f.write(screenshot)



# img_fp = 'screenshot.png'
# ocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
# out = ocr.ocr(img_fp)

# print(out)
