import json
import requests
from bs4 import BeautifulSoup
from Models.RequestModel import RequestModel


class Parser:

    @staticmethod
    def search(search_word):
        pass

class RadugastroyParser(Parser):

    @staticmethod
    def search(search_word):
        html = requests.get('https://radugastroy.ru/search/?module=search&action=search&searchword=' + search_word).text
        soup = BeautifulSoup(html, "html.parser")

        address = soup.find('div', {'class': 'siteFooter-address'}).text

        result = []
        for block in soup.find_all("li", {"class": "shopBlock-item"}):
            link = block.find("div", {"class": "name"}).find("a")
            name = link.text
            url = link.get('href')
            price = block.find("b", {"class": "js_shop_price"}).text

            if block.find("div", {"class": "stock js_stock inStock"}) is None:
                continue

            result.append(RequestModel(
                search_word,
                url,
                name,
                price,
                None,
                0,
                [address.strip()]
            ))

        return result


class SdvorParser(Parser):

    @staticmethod
    def search(search_word):
        cities = requests.get('https://www.sdvor.com/api/omni_order/cities/').text
        cities = json.loads(cities)

        addresses = []
        for city in cities:
            addresses.append(city['name'])

        items = {}

        for city in cities:
            html = requests.get(
                'https://www.sdvor.com/' + city['uri_name'] + '/search/?only_in_stock=true&str=' + search_word).text
            soup = BeautifulSoup(html, "html.parser")
            for block in soup.find_all("div", {"class": "w1l5ijvb p4t3w1l".split()}):
                identity = block.find('span', {'class': 'p1gaa8sl'}).text
                if identity in items:
                    continue

                link = block.find("div", {"class": "i1b5ubz7"}).find("a")
                url = 'https://www.sdvor.com/' + link.get('href')
                name = link.text

                price_elem = block.find("span", {"class": "p1hbhc78"})
                if price_elem is None:
                    continue
                price = price_elem.text.replace(' ₽', '')

                items[identity] = RequestModel(
                    search_word,
                    url,
                    name,
                    price,
                    None,
                    0,
                    addresses
                )

        result = []

        for key, value in items.items():
            result.append(value)

        return result


class Sb1Parser(Parser):

    @staticmethod
    def search(search_word):

        addresses = []

        soup2 = BeautifulSoup(requests.get('https://s-b-1.ru/contacts/').text, "html.parser")

        for city in soup2.find('table', {'class': 'contacts-stores no-border shops list'.split()}).find_all('tr'):
            if city.get("class") is not None:
                continue

            addresses.append(city.find('h4').text)

        html = requests.get('https://s-b-1.ru/catalog/?q=' + search_word).text
        soup = BeautifulSoup(html, "html.parser")

        result = []
        for block in soup.find_all("div", {"class": "item_block"}):
            title = block.find("div", {"class": "item-title"})
            name = title.find("span").text
            price = block.find("span", {"class": "price_value"}).text
            item_stock = block.find("div", {"class": "item-stock"})

            url = 'https://s-b-1.ru/' + title.find('a').get('href')

            if item_stock.find("span", {"class": "value"}).text == "Нет в наличии":
                continue

            result.append(RequestModel(
                search_word,
                url,
                name,
                price,
                None,
                0,
                addresses
            ))

        return result


parsers = [RadugastroyParser, SdvorParser, Sb1Parser]
