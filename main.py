
from pyppeteer import launch
from cnocr import CnOcr
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
from io import BytesIO
import pytesseract
import numpy as np

chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximize the browser window
chrome_options.add_argument("--disable-infobars")  # Disable the info bar
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-gpu")  # Disable the GPU
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable the DevShmUsage
chrome_options.add_argument("--no-sandbox")  # Disable the sandbox
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a window)
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sigapp.org/sac/sac2023/")  # Replace with the desired website URL

# Get the total height of the page
total_height = driver.execute_script("return document.body.scrollHeight")

# Set the window size to the total height
driver.set_window_size(1920, total_height)

# Take a screenshot of the visible area
screenshot = driver.get_screenshot_as_png()
image = Image.open(BytesIO(screenshot))
image.save("screenshot_long.png")

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def recognize_text_with_coordinates(image_path):
    image = Image.open(image_path)
    result = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    textimp=["IMPORTANT","Important","important"]
    textdate=["DATE","DATES","Date","Dates","date","dates"]
    yimp=0
    ydate=0
    count=0
    for i, text in enumerate(result['text']):
        if text and text.isalnum():
            left = result['left'][i]
            top = result['top'][i]
            width = result['width'][i]
            height = result['height'][i]
            print(f"Text: {text} (X: {left}, Y: {top}, Width: {width}, Height: {height})")
            if text in textimp:
                yimp=top
                count+=1
            if text in textdate:
                ydate=top
                count+=1
            if count==2 and (yimp<=ydate+10 or yimp>=ydate-10):
                break
    return yimp


def recognize_text_with_coordinates_dates(image_path):
    count=0
    image = Image.open(image_path)
    result = pytesseract.image_to_string(image, lang='eng')
    
    resultstring=result.split('\n')
    print(resultstring)
    # for text in resultstring:
    #     if count==1:
    #         print(text)
    #         count=0
    #     if text == "Abstract Due:":
    #         count=1
    #         print(text)
    #print(test)
    textabstract=["ABSTRACT","Abstract","Monday"]
    # textdate
    # for i, text in enumerate(result['text']):
    #     if text and text.isalnum():
    #         left = result['left'][i]
    #         top = result['top'][i]
    #         width = result['width'][i]
    #         height = result['height'][i]
    #         print(f"Text: {text} (X: {left}, Y: {top}, Width: {width}, Height: {height})")
    #         if text in textabstract:
    #             print(top)
    #         # if text in textlist:
    #         #     break
    # # return top

image_path = 'screenshot_long.png'  # 替換為你要辨識的圖片檔案路徑
yimp=recognize_text_with_coordinates(image_path)
print(yimp)
driver.set_window_size(1920, 1080)
driver.execute_script(f"window.scrollTo(0, {yimp-150});")
screenshot = driver.get_screenshot_as_png()
image = Image.open(BytesIO(screenshot))
image.save("screenshot_short.png")
driver.quit()


image = cv2.imread('screenshot_short.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('screenshot_short_21.png', gray_image)


image_path = 'screenshot_short_21.png'  # 替換為你要辨識的圖片檔案路徑
recognize_text_with_coordinates_dates(image_path)


# ocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
# out = ocr.ocr(image_path)

# print(out)