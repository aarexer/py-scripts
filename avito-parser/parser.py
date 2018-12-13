import requests
from bs4 import BeautifulSoup
import re
import csv
import os.path
import time

BASE_URL = 'https://www.avito.ru'
URL = 'https://www.avito.ru/moskva/avtomobili/vaz_lada/2109?radius=0&sgtd=5'
QUERY_URL = 'https://www.avito.ru/moskva/avtomobili/vaz_lada/2109?p={}&radius=0'
STORE_FILE_NAME = 'vaz2109.csv'


class Advert:
    def __init__(self, price, description, link):
        self._price = price
        self._description = description
        self._link = link

    def __repr__(self):
        return 'Price: {}, Description: {}, Link: {}'.format(self._price, self._description, self._link)


def get_html(url):
    request = requests.get(url)
    return request.text


def get_adverts(page_html):
    bs = BeautifulSoup(page_html, 'lxml')
    catalog_list = bs.find('div', class_='catalog-list js-catalog-list clearfix')

    before_ads_div = catalog_list.find('div', class_='js-catalog_before-ads')
    after_ads_div = catalog_list.find('div', class_='js-catalog_after-ads')

    before_ads = before_ads_div.find_all('div', class_='item_table')
    after_ads = after_ads_div.find_all('div', class_='item_table')

    return before_ads + after_ads


def create_advert(advert):
    price_span = advert.find('span', class_='price').text.strip()
    price = re.sub('\D', '', price_span)
    description = advert.find('div', class_='specific-params specific-params_block').text.strip()
    link = BASE_URL + advert.find('a', class_='item-description-title-link').get('href')

    return Advert(price, description, link)


def is_actual_data():
    """
    Return true if file with data isn't older than 30 minutes, otherwise - false.
    """
    return (current_time - os.path.getctime(STORE_FILE_NAME)) < 30 * 60


if __name__ == "__main__":
    adverts = []
    current_time = time.time()

    # if file exists and it's not older than 30 minutes - get data from file, otherwise - parse avito site again
    if os.path.isfile(STORE_FILE_NAME) and is_actual_data():
        with open(STORE_FILE_NAME, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for line in reader:
                adverts.append(Advert(line[0], line[1], line[2]))
    else:
        soup = BeautifulSoup(get_html(URL), 'lxml')
        last_page = soup.find('div', class_='pagination').find_all('a', class_='pagination-page')[-1]
        total_pages = int(last_page.get('href').split('=')[1].split('&')[0])

        for i in range(1, total_pages + 1):
            html_page = get_html(QUERY_URL.format(i))
            html_adverts_on_page = get_adverts(html_page)
            for ad in html_adverts_on_page:
                adverts.append(create_advert(ad))

        with open(STORE_FILE_NAME, 'w', newline='') as csvfile:
            reader = csv.writer(csvfile, delimiter=';')
            for advert in adverts:
                reader.writerow([advert._price, advert._description, advert._link])

    print('Adverts: {}\n'.format(len(adverts)))
    for advert in adverts:
        print(advert)
