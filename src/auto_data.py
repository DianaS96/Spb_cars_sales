import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from bs4 import BeautifulSoup
import requests
import lxml
import csv
import yaml

config = yaml.safe_load(open("C:/Users/User/Desktop/Programming/Spb_cars_sales/config/config.yaml"))['database']

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
    return max_page


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
        print(f"Page {i} processed")


# Creating file with links on ads
def create_file():
    with open(config['DIR'] + config['TXT_FILE'], "a") as file:
        for link in auto_urls:
            link_auto = "https://rolf-probeg.ru" + link
            file.write(f"{link_auto}\n")
        

# Collecting info on each auto
def get_info():
    with open(config['DIR'] + config['TXT_FILE']) as file:
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
                print(f"Smth is wrong with HTML ({line})")
                continue

            try:
                auto = soup.find('h1', class_="xl:text-[24px] text-[20px] xl:leading-[1.4] leading-snug").text.strip(' \n')
            except:
                print(f"There is no ad ({line})")
                continue

            try:
                auto_price = soup.find(class_="three-prices").find('div').find('span').text.strip(' \n')
            except:
                print(f"There is no price ({line})")
                continue

            try:
                auto_char_name = soup.find(class_="lg:ml-4 mt-9").find_all('ul')[0].find_all('li')
                auto_char = soup.find(class_="lg:ml-4 mt-9").find_all('ul')[1].find_all('li')
            except:
                auto_char = None
                auto_char_name = None

            auto_year = None
            auto_owners = 1
            auto_guarantee = None
            auto_mileage = None
            auto_engine = None
            auto_transmission = None
            auto_drive_unit = None
            auto_wheel = None
            auto_carcase = None
            auto_color = None
            for row in range(len(auto_char_name)):
                auto_year_col = auto_char_name[row].text.strip(' \n')
                if auto_year_col == 'Год выпуска':
                    auto_year = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Владельцы':
                    auto_owners = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Гарантия':
                    auto_guarantee = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Пробег':
                    auto_mileage = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Двигатель':
                    auto_engine = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Коробка':
                    auto_transmission = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Привод':
                    auto_drive_unit = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Руль':
                    auto_wheel = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Кузов':
                    auto_carcase = auto_char[row].text.strip(' \n')
                if auto_year_col == 'Цвет':
                    auto_color = auto_char[row].text.strip(' \n')

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

            with open(config['DIR'] + config['CSV_FILE'], "a", encoding="UTF-8-sig", newline="") as csv_file:
                write = csv.writer(csv_file, delimiter=';')
                if count == 1:
                    write.writerow(fields)
                write.writerow(rent_rows)
            print(str(count) + " out of " + str(length))
            count += 1


def get_auto_data():
    if config['update_auto_urls']:
        print("Collecting urls...")
        max_page = int(find_pages())
        get_links(max_page)
        create_file()
    get_info()
