import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests
import lxml
import csv
from fake_useragent import UserAgent


# Эти два заголовка нам нужны для того, чтобы сайт думал, что мы реальные пользователи
HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

auto_urls = list()


# Find number of pages with advertisements
def find_pages():
    i = 0
    url = f"https://rolf-probeg.ru/spb/cars/"
    url_content = requests.get(url, headers=HEADERS).content
    tree = BeautifulSoup(url_content, 'lxml')
    pagination = tree.find_all(class_='pagination-item')
    max_page = pagination[-1].text
    return (max_page)


# Collecting file with links on ads
def get_links(max_page):
    for i in range(1, max_page):

        url = f"https://rolf-probeg.ru/spb/cars/page/{i}/#cars"

        q = requests.get(url, headers=HEADERS)
        result = q.content

        soup = BeautifulSoup(result, "lxml")
        ads = soup.find_all(class_="card-car")

        for ad in ads:
            ad_url = ad.get("href")
            auto_urls.append(ad_url)


# Creating file with links on ads
def create_file():
    with open("auto_urls_list.txt", "a") as file:
        for link in auto_urls:
            link_auto = "https://rolf-probeg.ru/" + link
            file.write(f"{link_auto}\n")
        

# Collecting info on each apartment
def get_info():
    with open("auto_urls_list.txt") as file:
        lines = [line.strip() for line in file.readlines()]
        length = len(lines)
        count = 1

        for line in lines:
            url_auto = line
            try:
                q = requests.get(url_auto, headers=HEADERS)
                result = q.content
                soup = BeautifulSoup(result, 'html.parser')
            except:
                continue

            try:
                auto = soup.find('h1', class_="xl:text-[24px] text-[20px] xl:leading-[1.4] leading-snug").text
            except:
                auto = None

            try:
                auto_price = soup.find(class_="three-prices").find('div').find('span').text
            except:
                auto_price = None

            try:
                auto_char = soup.find(class_="lg:ml-4 mt-9").find_all('ul')[1].find_all('li')
            except:
                auto_char = None

            try:
                auto_year = auto_char[2].text
            except:
                auto_year = None

            try:
                auto_owners = auto_char[0].text
            except:
                auto_owners = None

            try:
                auto_guarantee = auto_char[1].text
            except:
                auto_guarantee = None

            try:
                auto_mileage = auto_char[3].text
            except:auto_mileage = None

            try: auto_engine = auto_char[4].text
            except: auto_engine = None

            try: auto_transmission = auto_char[5].text
            except:auto_transmission = None

            try: auto_drive_unit = auto_char[6].text
            except: auto_drive_unit = None

            try: auto_wheel = auto_char[7].text
            except: auto_wheel = None

            try: auto_carcase = auto_char[8].text
            except: auto_carcase = None

            try: auto_color =  auto_char[9].text
            except: auto_color = None

            data = {
                "Type": auto,
                "auto_price": auto_price,
                "auto_year": auto_year,
                "auto_owners": auto_owners,
                "auto_guarantee": auto_guarantee,
                "auto_mileage": auto_mileage,
                "auto_engine": auto_engine,
                "auto_transmission": auto_transmission,
                "auto_drive_unit": auto_drive_unit,
                "auto_wheel": auto_wheel,
                "auto_carcase": auto_carcase,
                "auto_color": auto_color,
                "link": url_auto
            }
            if count == 1:
                fields = data.keys()
            rent_rows = data.values()

            with open("auto_data.csv", "a", encoding="UTF-8-sig", newline="") as csv_file:
                write = csv.writer(csv_file, delimiter=';')
                if count == 1:
                    write.writerow(fields)
                write.writerow(rent_rows)
            print(str(count) + "out of " + str(length))
            count += 1

if __name__ == "__main__":
    #max_page = (int)(find_pages())
    #get_links(max_page)
    #create_file()
    get_info()

"""   rent_price = soup.find('span', itemprop="price").text
       rent_info_sq = soup.find_all(class_="a10a3f92e9--info-value--bm3DC")
       rent_space_total = rent_info_sq[0].text
       rent_space_living = rent_info_sq[1].text
       rent_space_kitchen = rent_info_sq[2].text
       rent_space_floor = rent_info_sq[3].text
   #    rent_year = rent_info_sq[4].text
       try:
           rent_station_1 = soup.find_all('a', class_='a10a3f92e9--underground_link--Sxo7K')[0].text
           rent_time_1 = soup.find_all('a', class_='a10a3f92e9--underground_time--iOoHy')[0].text
       except:
           rent_station_1 = 'N/A'
           rent_time_1 = 'N/A'

       try:
           rent_station_2 = soup.find_all('a', class_='a10a3f92e9--underground_link--Sxo7K')[1].text
           rent_time_2 = soup.find_all('a', class_='a10a3f92e9--underground_time--iOoHy')[1].text

       except:
           rent_station_2 = 'N/A'
           rent_time_2 = 'N/A'
       try:
           rent_station_3 = soup.find_all('a', class_='a10a3f92e9--underground_link--Sxo7K')[2].text
           rent_time_3 = soup.find_all('a', class_='a10a3f92e9--underground_time--iOoHy')[2].text
       except:
           rent_station_3 = 'N/A'
           rent_time_3 = 'N/A'
       rent_address = soup.find(class_="a10a3f92e9--geo--VTC9X").get('content')
"""

"""    "rent_price": rent_price,
     #  "rent_year": rent_year,
       "rent_space_total": rent_space_total,
       "rent_space_living": rent_space_living,
       "rent_space_kitchen": rent_space_kitchen,
       "rent_space_floor": rent_space_floor,
       "rent_station_1": rent_station_1,
       "rent_time_1": rent_time_1,
       "rent_station_2": rent_station_2,
       "rent_time_2": rent_time_2,
       "rent_station_3": rent_station_3,
       "rent_time_3": rent_time_3,
       "rent_address": rent_address
       """

