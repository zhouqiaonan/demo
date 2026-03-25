import requests
from lxml import etree


class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset=50'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}

    def save_html(self):
        html = requests.get(self.url, headers=self.headers).text
        parse_html = etree.HTML(html)

        dd_list = parse_html.xpath('//dl[@class="board-wrapper"]/dd')
        print(dd_list)
        item = {}
        for dd in dd_list:
            item["name"] = dd.xpath('.//p[@class="name"]/a/text()')[0].strip()
            item["star"] = dd.xpath('.//p[@class="star"]/text()')[0].strip()
            item["releasetime"] = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()
            print(item)
    def run(self):
        self.save_html()

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.run()