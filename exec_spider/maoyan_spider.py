import json
import random
import re
import time
from datetime import datetime
from urllib import request

import pymysql
import requests


class MaoyanSpider(object):
    def __init__(self):
        self.url = 'http://www.maoyan.com/board/4?offset={}'

    def gen_uuid(self):
        # 生成随机数（对应 JavaScript 的 Math.random() * Number.MAX_SAFE_INTEGER）
        random_part = random.randint(0, 2 ** 53 - 1)  # Number.MAX_SAFE_INTEGER = 2^53 - 1
        # 转换为十六进制字符串
        random_hex = hex(random_part)[2:]  # [2:] 去掉 '0x' 前缀

        # 获取当前时间戳（毫秒），对应 JavaScript 的 new Date().getTime()
        timestamp = int(time.time() * 1000)
        timestamp_hex = hex(timestamp)[2:]

        # 拼接结果
        return f"{random_hex}-{timestamp_hex}"

    def get_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",}
        # req = request.Request(url=url, headers=headers)
        cookies = {"uuid": str(self.gen_uuid())}
        resp = requests.get(url=url, headers=headers, cookies=cookies)
        print(resp.text)
        print(resp.status_code)
        print(url)
        # res = request.urlopen(req)
        # print(res.read())
        # html = res.read().decode()
        # print(html)
        html = resp.content
        with open('maoyan_verify.html', 'wb') as f:
            f.write(html)
        self.parse_html(html)

    def parse_html(self, html):
        re_bds = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>'
        pattern = re.compile(re_bds, re.S)

        r_list = pattern.findall(html.decode("utf-8"))
        # print(r_list)
        self.save_html(r_list)

    def save_html(self, r_list):
        new_list = []
        for item in r_list:
            processed_item  = self._process_item(item)
            new_list.append(" ".join(processed_item))
            self.sql_insert(processed_item)
        print(new_list)
        with open('maoyan_verify.csv', 'a+', encoding="utf-8") as f:
            for i in new_list:
                f.write(i + '\n')

    def _process_item(self, item):
        res_lst = []
        for i in item:
            i_list = i.strip().split('：')
            if len(i_list) == 2:
                new_time = self.recursion_time(i_list[1])
                res_lst.append(new_time)
            else:
                res_lst.append(i_list[0])
        print(res_lst)
        res_lst = self.deal_time(res_lst)
        return res_lst

    def deal_time(self, res_lst):
        create_time = res_lst.pop()
        if len(create_time.split("-")) == 1:
            create_time = f"{create_time}-1-1"
        res_lst.append(create_time)
        return res_lst

    def recursion_time(self, create_time):
        if "(" in create_time:
            new_time = create_time.split("(")[0]
        else:
            new_time = create_time

        return new_time

    def sql_insert(self, info_list):
        db = pymysql.connect(host="localhost", user="user", password="password", db="my_database")
        cursor = db.cursor()
        # info_list = ["我不是药神", "徐峥,王传君,周一围", "2018-07-05"]
        sql = "insert into movieinfo values (%s, %s, %s)"
        cursor.execute(sql, info_list)
        db.commit()
        cursor.close()
        db.close()

    def run(self):
        for offset in range(0, 100, 10):
            url = self.url.format(offset)
            self.get_html(url)
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    try:
        spider = MaoyanSpider()
        spider.run()
        # spider.sql_insert()
    except Exception as e:
        print(e)