from bs4 import BeautifulSoup
import re
from duckduckgo_search import DDGS
from itertools import islice
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

time="2024"

file_path = "full_list.csv"
with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        combinekey=str(row[0]+" "+row[1])
        conf_name=row[1]
        full_name=row[4]

        searchkey = str(time)+" "+combinekey+" home website"
        print(searchkey)
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(searchkey, region='tw-tzh')
            for r in islice(ddgs_gen, 3):
                # print(full_name)
                print(r["href"])
                with open("link.txt", "a") as file:
                    file.write(str(combinekey)+","+str(r["href"])+"\n")
            print("檔案寫入完成.")
        
        # searchkey = str(time)+" "+full_name+" home website"
        # print(searchkey)
        # with DDGS() as ddgs:
        #     ddgs_gen = ddgs.text(searchkey, region='tw-tzh')
        #     for r in islice(ddgs_gen, 3):
        #         # print(full_name)
        #         print(r["href"])
        #         with open("link.txt", "a") as file:
        #             file.write(str(combinekey)+","+str(r["href"])+"\n")
        #     print("檔案寫入完成.")

        # searchkey = str(time)+" "+full_name+" Call for Papers/Call for Contributions website"
        # print(searchkey)
        # with DDGS() as ddgs:
        #     ddgs_gen = ddgs.text(searchkey, region='tw-tzh')
        #     for r in islice(ddgs_gen, 3):
        #         # print(full_name)
        #         print(r["href"])
        #         with open("link.txt", "a") as file:
        #             file.write(str(combinekey)+","+str(r["href"])+"\n")
        #     print("檔案寫入完成.")