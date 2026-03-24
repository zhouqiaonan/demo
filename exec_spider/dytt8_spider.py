import re
import time
from hashlib import md5

import pymysql
import requests


class MovieSkySpiker(object):
    def __init__(self):
        self.url = "https://dytt8.com/html/gndy/dyzz/list_23_{}.html"
        self.db = pymysql.connect(host="localhost", user="root", password="rootpassword", db="movieskydb")
        self.cursor = self.db.cursor()

    def get_html(self, url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        }
        req = requests.get(url, headers=headers)
        html = req.content
        with open("dytt8.html", "wb") as f:
            f.write(html)
        return html.decode('gbk')

    def re_func(self, re_bds, html):
        r_list = re.findall(re_bds, html)
        return r_list

    def parse_html(self, one_url):
        one_html = self.get_html(one_url)
        re_bds = '<a href="(.*?)".*?class="ulink">(.*?)</a>'
        link_list = self.re_func(re_bds, one_html)
        print(link_list)
        for link in link_list:
            two_url = f"https://dytt8.com{link[0]}"
            s = md5()
            s.update(two_url.encode())
            finger = s.hexdigest()
            if self.is_hold_on(finger):
                self.save_html(two_url)
                time.sleep(1)
                ins = "insert into request_finger values (%s)"
                self.cursor.execute(ins, [finger,])
                self.db.commit()

    def is_hold_on(self, finger):
        sql = f"select finger from request_finger where finger=%s"
        r = self.cursor.execute(sql, [finger])
        if not r:
            return True

    def save_html(self, two_url):
        two_html = self.get_html(two_url)
        re_bds = r'<div class="title_all">[\s\S]*?<a href=\'(.*?)\'>(.*?)</a>'
        re_list = self.re_func(re_bds, two_html)
        print(re_list)
        film_list = []
        for re in re_list:
            film = list(re)
            film[0] = f"https://dytt8.com{film[0]}"
            film_list.append(film)
        sql = "insert into movieinfo(downloadaddr,moviename) values(%s,%s)"
        self.cursor.executemany(sql, film_list)
        self.db.commit()


    def run(self):
        for i in range(1, 2):
            url = self.url.format(i)
            self.parse_html(url)


if __name__ == '__main__':
    spider = MovieSkySpiker()
    spider.run()