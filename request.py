import requests
from bs4 import BeautifulSoup
import re

# 發送HTTP GET請求
url = "https://www.sigapp.org/sac/sac2023/"  # 要爬取的網站URL
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.get_text()
    clean_string = re.sub(r"\n", "", content)
    print(clean_string)
    # # 範例：從HTML中擷取所有連結
    # links = soup.find_all('a')  # 找到所有<a>標籤

    # # 輸出擷取結果
    # for link in links:
    #     print(link['href'])

else:
    print("無法連接到網站")