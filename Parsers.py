import requests
from bs4 import BeautifulSoup


# TODO - Никита, если не сложно можешь подогнать методы search так, чтобы они возвращали объекты класса ResultModel :)

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

        for block in soup.find_all("li", {"class": "shopBlock-item"}):
            name = block.find("div", {"class": "name"}).find("a").text
            price = block.find("b", {"class": "js_shop_price"}).text

            in_stock = "+"
            if block.find("div", {"class": "stock js_stock inStock"}) is None:
                in_stock = "-"

            print(name + " (" + price + ")  " + in_stock)


class SdvorParser:

    @staticmethod
    def search(search_word):
        html = requests.get('https://www.sdvor.com/moscow/search/?only_in_stock=true&str=' + search_word).text
        soup = BeautifulSoup(html)

        categories = []
        for category in soup.find("ul", {"class": "lkhh32y"}).find_all("li"):
            category = category.find('a', {"class": "lf4rfcn l1f0l9hb a1pqe0q7"})
            if category is None:
                break
            categories.append(category.text)

        for block in soup.find_all("div", {"class": "w1l5ijvb p4t3w1l".split()}):
            name = block.find("div", {"class": "i1b5ubz7"}).find("a").text
            price = block.find("span", {"class": "p1hbhc78"}).text
            in_stock = "+"
            print(name + " (" + price + ")  " + in_stock)


class Sb1Parser:

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