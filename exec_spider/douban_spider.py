import json
import time
from wsgiref import headers

import requests
from lxml import etree


class DoubanSpider:
    def __init__(self):
        self.url = "https://movie.douban.com/j/chart/top_list?"
        self.i = 0

    def get_headers(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",}
        return headers

    def get_all_type_films(self):
        url = "https://movie.douban.com/chart"
        headers = self.get_headers()
        html = requests.get(url=url, headers=headers).text
        # print(html)
        parse_html = etree.HTML(html)
        type_list = parse_html.xpath('//div[@class="types"]/span/a/@href')
        # print(type_list)
        type_dict = {}
        menus = []
        for type_str in type_list:
            type_str = type_str.strip()
            params = type_str.split('?')[1].split("&")[:2]
            type_name = params[0].split("=")[1]
            type_number = params[1].split("=")[1]
            type_dict[type_name] = type_number
            menus.append(type_name)
        menu = ",".join(menus)
        return type_dict, menu

    def total_number(self, type_number):
        url = f"https://movie.douban.com/j/chart/top_list_count?type={type_number}&interval_id=100%3A90"
        headers = self.get_headers()
        html = requests.get(url=url, headers=headers).json()
        total = int(html["total"])
        return total

    def parse_page(self, html):
        item = {}
        for one in html:
            item["name"] = one["title"].strip()
            item["score"] = one["score"]
            print(item)
            self.i += 1

    def get_page(self, params):
        html = requests.get(url=self.url, headers=self.get_headers(), params=params).text

        html = json.loads(html)
        self.parse_page(html)

    def main(self):
        type_dict, menu = self.get_all_type_films()
        menu = menu + '\n你想了解什么类型电影:'
        name = input(menu)
        type_number = type_dict[name]
        print(type_number)
        total = self.total_number(type_number)
        print(total)
        for start in range(0, total + 1, 20):
            params = {
                "type": type_number,
                "interval_id": "100:90",
                "action": "",
                "start": start,
                "limit": 20
            }
            self.get_page(params)
            time.sleep(1)
        print(f"电影总数量: {self.i}")


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.main()
