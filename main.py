
from pyppeteer import launch
from cnocr import CnOcr
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
from io import BytesIO
import pytesseract

chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximize the browser window
chrome_options.add_argument("--disable-infobars")  # Disable the info bar
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-gpu")  # Disable the GPU
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable the DevShmUsage
chrome_options.add_argument("--no-sandbox")  # Disable the sandbox
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a window)
#chrome_options.add_argument("--force-device-scale-factor=1")  # Set the zoom level to 150%
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
image.save("screenshot_0.png")

# # Scroll down the page and capture additional screenshots
# scroll_height = 1080  # Adjust this value based on your desired scrolling increment
# current_height = 1080
# counter=1
# while current_height < total_height:
#     driver.execute_script(f"window.scrollTo(0, {current_height});")
#     screenshot = driver.get_screenshot_as_png()
#     image = Image.open(BytesIO(screenshot))
#     image.save(f"screenshot_{counter}.png")
#     current_height += scroll_height
#     counter+=1

# Close the browser
driver.quit()

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def recognize_text_with_coordinates(image_path):
    image = Image.open(image_path)
    result = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    for i, text in enumerate(result['text']):
        if text and text.isalnum():
            left = result['left'][i]
            top = result['top'][i]
            width = result['width'][i]
            height = result['height'][i]
            print(f"Text: {text} (X: {left}, Y: {top}, Width: {width}, Height: {height})")
            if 

image_path = 'screenshot_0.png'  # 替換為你要辨識的圖片檔案路徑
recognize_text_with_coordinates(image_path)













# img_fp = 'screenshot0.png'
# ocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
# out = ocr.ocr(gray_image)