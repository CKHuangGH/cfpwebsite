import duckduckpy
from bs4 import BeautifulSoup
import requests
import re
from duckduckgo_search import DDGS
from itertools import islice
num_results = 1
stop=1
conflist=[]

file_path = "list.txt"
with open(file_path, 'r') as file:
    lines = file.readlines()
lines = [line.strip() for line in lines]

for conf in lines:
    query = conf+" "+"2024"+" HOME"
    print(query)

    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(query, region='tw-tzh')
        for r in islice(ddgs_gen, 2):
            print(r["href"])











    #search_results = search(query, num_results=1)
    # search_results=search_duckduckgo(query)
    # print(search_duckduckgo)
    # # for result in search_results:
    #     response = requests.get(result)
    #     if response.status_code == 200:
    #         content = response.text
            
    #         soup = BeautifulSoup(content, 'html.parser')
    #         content = soup.get_text()
    #         string= '\n'.join(soup.stripped_strings)
    #         for text in string.splitlines():
    #             print(text)
