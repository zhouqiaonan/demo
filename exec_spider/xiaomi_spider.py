import csv
import time
from queue import Queue
from threading import Thread, Lock

import requests
from lxml import etree


class XiaomiSpider:
    def __init__(self):
        self.url = "http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30"
        self.q = Queue()
        self.i = 0
        self.id_list = []
        self.f = open("XiaomiShangcheng.csv", "a+", newline='', encoding="utf-8")
        self.writer = csv.writer(self.f)
        self.lock = Lock()

    def get_headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", }
        return headers

    def get_cateid(self):
        raw_url = "https://app.mi.com"
        url = f"{raw_url}/allCloudGames"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", }
        html = requests.get(url, headers=headers).text
        parse_html = etree.HTML(html)

        page_bds = '//div[@class="pages"]//a/text()'
        page_list = parse_html.xpath(page_bds)
        page_nums = []
        for page in page_list:
            if page.isdigit():
                page_nums.append(int(page))
        if page_nums:
            total_page_num = max(page_nums)
        else:
            total_page_num = 1
        print(total_page_num)
        for i in range(1, total_page_num + 1):
            new_url = f"{url}?page={i}"
            html = requests.get(new_url, headers=headers).text
            xpath_bds = '//ul[@class="applist index-cloud-list"]'
            parse_html = etree.HTML(html)
            li_list = parse_html.xpath(xpath_bds)
            print(li_list)
            for li in li_list:
                href_lst = li.xpath('./li/h5/a/@href')
                name_lst = li.xpath('./li/h5/a/text()')
                print(name_lst)
                for idx, href in enumerate(href_lst):
                    print(name_lst[idx])
                    all_href = f"{raw_url}{href}"
                    self.q.put(all_href)


    def get_data(self):
        app_lst = []
        while self.q.qsize() > 0:
            url = self.q.get()
            # print(url)
            headers = self.get_headers()
            html = requests.get(url, headers=headers).text
            parse_html = etree.HTML(html)
            name, category, link = self.parse_html(parse_html, url)
            if name and category and link:
                app_lst.append([name, category, link])
                self.i += 1
        print(app_lst)
        for app in app_lst:
            self.lock.acquire()
            self.writer.writerow(app)
            self.lock.release()

    def parse_html(self, parse_html, url):
        link_lst = parse_html.xpath('//div[@class="line-break"]/text()')
        link_lst = [i.strip() for i in link_lst]
        # print(link_lst)
        category_lst = parse_html.xpath('//div[@class="bread-crumb"]/ul/li/a/text()')
        name_lst = parse_html.xpath('//div[@class="bread-crumb"]/ul/li/text()')
        name_lst = [i.strip() for i in name_lst if i.strip()]
        # print(name_lst)
        # print(category_lst)
        name = name_lst[0] if name_lst else ""
        category = category_lst[1] if len(category_lst) >= 2 else ""
        link = link_lst[0] if link_lst else ""
        link = f"https://app.mi.com/details?id={link}"
        print(name, category, link, url)
        return name, category, link



    def main(self):
        self.get_cateid()
        t_list = []
        for i in range(1):
            t = Thread(target=self.get_data)
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()
        self.f.close()
        print(f"数量: {self.i}")


if __name__ == '__main__':
    start = time.time()
    spider = XiaomiSpider()
    spider.main()
    end = time.time()
    print(f"执行时间: {end-start}")