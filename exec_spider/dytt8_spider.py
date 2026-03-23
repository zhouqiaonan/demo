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
        print(html)
        with open("dytt8.html", "wb") as f:
            f.write(html)
        return html

    def parse_html(self, one_url):
        one_html = self.get_html(one_url)

    def run(self):
        for i in range(1, 2):
            url = self.url.format(i)
            self.parse_html(url)


if __name__ == '__main__':
    spider = MovieSkySpiker()
    spider.run()