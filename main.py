from pyppeteer import launch
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
from io import BytesIO
import pytesseract
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

country_list = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia',
    'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
    'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria',
    'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad',
    'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
    'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor',
    'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji',
    'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala',
    'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
    'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
    'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
    'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia',
    'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand',
    'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau',
    'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
    'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
    'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan',
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
    'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda',
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'USA', 'Uruguay', 'Uzbekistan', 'Vanuatu',
    'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

full_month_names = ["January", "February", "March", "April", "May", "June", "July", "August", 
                    "September", "October", "November", "December",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", 
    'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 
    'OCTOBER', 'NOVEMBER', 'DECEMBER','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
full_years = ["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]
full_dates = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def checkdash(text):
    pattern = r'(\d+)-(\d+)'
    matches = re.findall(pattern, text)
    result = []
    for match in matches:
        result.append((int(match[0]), int(match[1])))
    return result

def recognize_country(image_path):
    data = pytesseract.image_to_data(image_path, output_type=pytesseract.Output.DICT)
    country=""
    dates=""
    mon=""
    year=""
    startdate=""
    enddate=""
    for i in range(len(data['text'])):
        text = data['text'][i]
        x = data['left'][i]
        y = data['top'][i]
        width = data['width'][i]
        height = data['height'][i]
        if text:
            if checkdash(text) and dates=="":
                dates=text.rstrip(",")
                #print(text)
            else: 
                text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            if text in full_dates and (startdate=="" or enddate==""):
                if startdate =="":
                    startdate=text
                else:
                    enddate=text
            if text in full_month_names and mon=="":
                mon=text
            if text in full_years and year=="":
                year=text
            if text in country_list and country=="":
                country=text
            if text:
                print('文字：', text)
                # print('座標位置：({},{}) - ({},{})'.format(x, y, x + width, y + height))
                # print('---')
    if dates!="":
        return dates,mon,year,country
    else:
        dates=str(startdate)+"-"+str(enddate)
        return dates,mon,year,country

def recognize_important(image_path,country):
    image = Image.open(image_path)
    result = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    textimp=["IMPORTANT","Important","important"]
    textdate=["DATE","DATES","Date","Dates","date","dates"]
    yimp=0
    ydate=0
    flag=0
    count=0
    for i, text in enumerate(result['text']):
        if text and text.isalnum():
            left = result['left'][i]
            top = result['top'][i]
            width = result['width'][i]
            height = result['height'][i]
            #print(f"Text: {text} (X: {left}, Y: {top}, Width: {width}, Height: {height})")
            if country!=" ":
                if text in country_list and flag!=1:
                    country=text
                    flag=1
            if text in textimp:
                yimp=top
                count+=1
            if text in textdate:
                ydate=top
                count+=1
            if count==2 and (yimp<=ydate+10 or yimp>=ydate-10):
                break
    return yimp,country

def recognize_dates(image_path):
    data = pytesseract.image_to_string(image_path, output_type=pytesseract.Output.DICT)
    print(data)
    resultstring=data
    for text in data['text']:
        print(text)



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

if __name__ == "__main__":
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("--start-maximized")  # Maximize the browser window
    # chrome_options.add_argument("--disable-infobars")  # Disable the info bar
    # chrome_options.add_argument("--disable-extensions")  # Disable extensions
    # # chrome_options.add_argument("--disable-gpu")  # Disable the GPU
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Disable the DevShmUsage
    # chrome_options.add_argument("--disable-cookies")
    # chrome_options.add_argument("--disable-storage-reset")
    # chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--no-sandbox")  # Disable the sandbox
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a window)
    # #chrome_options.add_argument("--window-size=1920,1080")
    
    # country=""
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.set_window_size(1920, 1080)
    # driver.get("https://infocom2023.ieee-infocom.org/")  # Replace with the desired website URL
    # time.sleep(5)
    # driver.execute_script(f"window.scrollTo(0, 0);")
    # screenshot = driver.get_screenshot_as_png()
    # image = Image.open(BytesIO(screenshot))
    # image.save("screenshot_first_area.png")
    # image = cv2.imread("screenshot_first_area.png")
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("screenshot_first_area_gray.png", gray_image)
    
    # dates,mon,year,country=recognize_country("screenshot_first_area_gray.png")
    # print(dates,mon,year,country)

    # # Get the total height of the page
    # total_height = driver.execute_script("return document.body.scrollHeight")

    # # Set the window size to the total height
    # driver.set_window_size(1920, total_height)

    # # Take a screenshot of the visible area
    # screenshot = driver.get_screenshot_as_png()
    # image = Image.open(BytesIO(screenshot))
    # image.save("screenshot_full.png")
    # image = cv2.imread("screenshot_full.png")
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("screenshot_full_gray.png", gray_image)

    # yimp,country=recognize_important("screenshot_full_gray.png",country)
    # driver.set_window_size(1920, 1080)
    # driver.execute_script(f"window.scrollTo(0, {yimp-100});")
    # screenshot = driver.get_screenshot_as_png()
    # image = Image.open(BytesIO(screenshot))
    # image.save("screenshot_importance_dates.png")
    # driver.quit()

    # image = cv2.imread("screenshot_importance_dates.png")
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("screenshot_importance_dates_gray.png", gray_image)
    recognize_dates("screenshot_importance_dates_gray.png")