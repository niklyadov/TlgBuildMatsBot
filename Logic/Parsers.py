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
            json_addresses = json.loads(requests.get('https://www.sdvor.com/api/omni_order/shops/?city_id={}'.format(city['id'])).text)
            for address in json_addresses:
                addresses.append(city['name'] + ' ' + address['address'])

        result = []

        for city in cities:
            html = requests.get(
                'https://www.sdvor.com/' + city['uri_name'] + '/search/?only_in_stock=true&str=' + search_word).text
            soup = BeautifulSoup(html, "html.parser")
            for block in soup.find_all("div", {"class": "w1l5ijvb p4t3w1l".split()}):
                link = block.find("div", {"class": "i1b5ubz7"}).find("a")
                name = link.text
                price = block.find("span", {"class": "p1hbhc78"}).text
                url = link.get('href')

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


class Sb1Parser(Parser):

    @staticmethod
    def search(search_word):
        html = requests.get('https://s-b-1.ru/catalog/?q=' + search_word).text
        soup = BeautifulSoup(html, "html.parser")

        addresses = []
        for city in soup.find('div', {'class': 'region_wrapper'}).find('div', {'ul': 'wrap'}).find_all('li', {
            'class': 'more_item has-sub'}):
            city_name = city.find('a', {'class': 'item none_click'.split()})
            for addresses_json in city.find('div', {'class': 'sub'}).find_all('li'):
                address_name = addresses_json.find('a', {'class': 'item'}).text
                addresses.append(city_name + " " + address_name)

        result = []
        for block in soup.find_all("div", {"class": "item_block"}):
            link = block.find("div", {"class": "item-title"})
            name = link.find("span").text
            price = block.find("span", {"class": "price_value"}).text
            item_stock = block.find("div", {"class": "item-stock"})
            url = link.get('href')

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
