import requests
from bs4 import BeautifulSoup


class CurrencyRow:
    def __init__(self, rank, name, link, price):
        self.name = name
        self.rank = rank
        self.link = link
        self.price = price

    def __str__(self) -> str:
        return "Name: {}, rank: {}, price: {}, link: {}".format(self.name, self.rank, self.price, self.link)


class CoinMarketCapScrapper:
    URL = 'https://coinmarketcap.com/all/views/all/'
    DOMAIN_NAME = 'https://coinmarketcap.com'

    def __init__(self, lazy=False):
        request = requests.get(self.URL)

        if request.status_code != 200:
            raise Exception("URL: {} is unavailable now".format(self.URL))

        self._html = request.text
        self._bs = BeautifulSoup(self._html, 'lxml')
        self.currencies_cache = []
        if not lazy:
            self.currencies_cache = self.currencies()

    def currencies(self):
        table = self._bs.find('table', id='currencies-all')
        table_body = table.find('tbody')

        trs = table_body.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            rank = tds[0].text.strip()

            td_name = tds[1].find('a', class_='currency-name-container')
            link = self.DOMAIN_NAME + td_name.get('href')
            name = td_name.text.strip()

            price = tds[4].text.strip()

            self.currencies_cache.append(CurrencyRow(rank, name, link, price))

        return self.currencies_cache
