import json
import venv

import requests
from bs4 import BeautifulSoup

# TODO - Никита, если не сложно можешь подогнать методы search так, чтобы они возвращали объекты класса ResultModel :)
from RequestModel import RequestModel


class Parser:

    @staticmethod
    def search(search_word):
        pass


class RadugastroyParser(Parser):

    @staticmethod
    def search(search_word):
        html = requests.get('https://radugastroy.ru/search/?module=search&action=search&searchword=' + search_word).text
        soup = BeautifulSoup(html)

        categories = []
        for category in soup.find_all("li", {"class": "shopListingPage-cat"}):
            categories.append(category.find("a").text)

        address = soup.find('div', {'class': 'siteFooter-address'}).text

        result = []
        for block in soup.find_all("li", {"class": "shopBlock-item"}):
            link = block.find("div", {"class": "name"}).find("a")
            name = link.text
            url = link.get('href')
            price = block.find("b", {"class": "js_shop_price"}).text

            if block.find("div", {"class": "stock js_stock inStock"}) is None:
                return

            result.append(RequestModel(
                search_word,
                url,
                name,
                price,
                None,
                0,
                {address}
            ))

        return result


class SdvorParser(Parser):

    @staticmethod
    def search(search_word):
        cities = requests.get('https://www.sdvor.com/api/omni_order/cities/').text
        cities = json.loads(cities)

        addresses = []
        for city in cities:
            for address in requests.get('https://www.sdvor.com/api/omni_order/shops/?city_id=' + city.id).text:
                address = json.loads(address)
                addresses.append(city.name + ' ' + address.address)

        html = requests.get('https://www.sdvor.com/moscow/search/?only_in_stock=true&str=' + search_word).text
        soup = BeautifulSoup(html)

        categories = []
        for category in soup.find("ul", {"class": "lkhh32y"}).find_all("li"):
            category = category.find('a', {"class": "lf4rfcn l1f0l9hb a1pqe0q7"})
            if category is None:
                break
            categories.append(category.text)

        result = []
        for block in soup.find_all("div", {"class": "w1l5ijvb p4t3w1l".split()}):
            name = block.find("div", {"class": "i1b5ubz7"}).find("a").text
            link = block.find("span", {"class": "p1hbhc78"})
            price = link.text
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


class Sb1Parser(Parser):

    @staticmethod
    def search(search_word):
        html = requests.get('https://s-b-1.ru/catalog/?q=' + search_word).text
        soup = BeautifulSoup(html)

        categories = []
        for category in soup.find("div", {"class": "top_block_filter_section"}) \
                .find("div", {"class": "items"}).find_all("div", {"class": "item"}):
            category = category.find('a')
            if category is None:
                break
            categories.append(category.find("span").text)

        for block in soup.find_all("div", {"class": "item_block"}):
            name = block.find("div", {"class": "item-title"}).find("span").text
            price = block.find("span", {"class": "price_value"}).text

            item_stock = block.find("div", {"class": "item-stock"})

            in_stock = "+"

            if item_stock.find("span", {"class": "value"}).text == "Нет в наличии":
                in_stock = "-"

            print(name + " (" + price + ")  " + in_stock)


parsers = [RadugastroyParser, SdvorParser, Sb1Parser]
