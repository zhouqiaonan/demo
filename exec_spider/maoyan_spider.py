import json
import random
import re
import time
from urllib import request

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
        for r in r_list:
            # print(r)
            new_str = ""
            new_i_list = []
            for i in r:
                # print(i.strip())
                i_list = i.strip().split('：')
                if len(i_list) == 2:
                    new_i_list.append(i_list[1])
                else:
                    new_i_list.append(i_list[0])
            new_list.append(" ".join(new_i_list))
        print(new_list)
        with open('maoyan_verify.csv', 'w', encoding="utf-8") as f:
            for i in new_list:
                f.write(i + '\n')

    def run(self):
        for offset in range(0, 2, 10):
            url = self.url.format(offset)
            self.get_html(url)
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    try:
        spider = MaoyanSpider()
        spider.run()
    except Exception as e:
        print(e)