import scrapy

from exec_spider.Maoyan100.Maoyan100.items import Maoyan100Item


class MaoyanSpider(scrapy.Spider):
    name = "maoyan"
    allowed_domains = ["www.maoyan.com"]
    start_urls = ["https://www.maoyan.com/board/4?offset=0"]
    offset = 0

    def parse(self, response):
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        item = Maoyan100Item()
        for dd in dd_list:
            item["name"] = dd.xpath('./a/@title').get().strip()
            item["star"] = dd.xpath('.//p[@class="score"]/i/text()')
            print("-" * 60)
            print(item)
            print("-" * 60)
