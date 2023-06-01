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
url = 'https://www.sigmobile.org/mobicom/2023/index.html'
loop = asyncio.get_event_loop()
screenshot = loop.run_until_complete(screenshot_full_page(url))

# 儲存截圖
with open('screenshot.png', 'wb') as f:
    f.write(screenshot)