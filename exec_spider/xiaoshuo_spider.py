import urllib
from email.header import Header

from bs4 import BeautifulSoup


def request_html(url):
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    req = urllib.request.Request(url, headers=Headers)
    return req


def parse_html(html, f):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


def run():
    url = "http://www.shicimingju.com/book/liangjinyanyi.html"
    f =  open("两晋演义.txt", "w", encoding="utf-8")
    request = request_html(url)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    parse_html(html, f)
    f.close()


if __name__ == '__main__':
    run()