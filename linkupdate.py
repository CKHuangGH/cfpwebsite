from bs4 import BeautifulSoup
import re
from duckduckgo_search import DDGS
from itertools import islice
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

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
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'UK', 'USA', 'Uruguay', 'Uzbekistan', 'Vanuatu',
    'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

full_month_names = ["January", "February", "March", "April", "May", "June", "July", "August", 
                    "September", "October", "November", "December", 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 
    'OCTOBER', 'NOVEMBER', 'DECEMBER', 'NOV']
full_years = ["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]

def checkdash(text):
    pattern = r'(\d+)\D*?(&ndash;|\-)\D*?(\d+)'
    matches = re.findall(pattern, text)
    print(matches)
    if matches:
        for match in matches:
            start_number = match[0]
            end_number = match[2]
            # print("起始數字:", start_number)
            # print("結束數字:", end_number)
            return start_number,end_number
    else:
        pattern = r'(\d+)\D*–\D*(\d+)'
        matches = re.findall(pattern, text)
        print(matches)
        if matches:
            for match in matches:
                start_number = match[0]
                end_number = match[1]
                # print("起始數字:", start_number)
                # print("結束數字:", end_number)
                return start_number,end_number
        return 0,0

# def csvhandle(text):

savestartnumber=0
saveendnumber=0
file_path = "full_list.csv"
with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        combinekey=str(row[0]+" "+row[1])
        conf_name=row[1]
        savestartnumber=""
        saveendnumber=""
        savemonth=""
        saveyear=""
        savecountry=""
        searchkey = combinekey+" 2024 conference/symposium home"
        print(searchkey)
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(searchkey, region='tw-tzh')
            for r in islice(ddgs_gen, 1):
                print(r["href"])
                savehref=r["href"]
                query=r["href"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(query)
        driver.implicitly_wait(5)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')
        text = soup.get_text(strip=True)
        string= '\n'.join(soup.stripped_strings)
        flag_country=0
        flag_month=0
        flag_year=0
        flag_dates=0
        savestartnumber=0
        saveendnumber=0

        for text in string.splitlines():
            if text.find(conf_name):
                checkwebsite=1
                print("website check ok")
                break

        if checkwebsite==1:
            for text in string.splitlines():
                # print(text)
                for country in country_list:
                    index = text.find(country)
                    if index != -1 and flag_country==0:
                        flag_country=1
                        savecountry=country
                        # print(country)
                for year in full_years:
                    index = text.find(year)
                    if index != -1 and flag_year==0:
                        flag_year=1
                        saveyear=year
                        # print(year)
                for month in full_month_names:
                    index = text.find(month)
                    if index != -1 and flag_month==0:
                        flag_month=1
                        savemonth=month
                        # print(month)
                if (("-" in text) or ("–" in text)) and flag_dates==0:
                    start_number,end_number=checkdash(text)
                    if start_number!=0 and end_number!=0:
                        flag_dates=1
                        savestartnumber=start_number
                        saveendnumber=end_number
                if (flag_dates+flag_country+flag_month+flag_year) == 4:
                    break  
        else:
            print("error")

        if (flag_dates+flag_country+flag_month+flag_year) >= 3:
            with open("output.txt", "a") as file:
                file.write(str(combinekey)+","+str(savestartnumber)+"-"+str(saveendnumber)+","+str(savemonth)+","+str(saveyear)+","+str(savecountry)+","+str(savehref)+"\n")
            print("檔案寫入完成.")