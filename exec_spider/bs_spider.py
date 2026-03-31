import re

from bs4 import BeautifulSoup
from lxml import html

# html_doc = """
# <html><head><title>"c语言中文网"</title></head>
# <body>
# <p class="title"><b>c.biancheng.net</b></p>
# <p class="website">一个学习编程的网站
# <a href="http://c.biancheng.net/python/" id="link1">python教程</a>
# <a href="http://c.biancheng.net/c/" id="link2">c语言教程</a>
# """
# soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

# soup = BeautifulSoup('<p class="Web site url"><b>c.biancheng.net</b></p>', 'html.parser')
# print(soup.p)
# print(soup.p.b)
# print(soup.p.text)
# print(soup.p.attrs)
# print(type(soup.p))
# print(soup.p["class"])
# soup.p["class"] = ["web", "site"]
# print(soup.p)
#
# html_doc = """
# <html><head><title>"c语言中文网"</title></head>
# <body>
# <p class="title"><b>c.biancheng.net</b></p>
# <p class="website">一个学习编程的网站</p>
# <a href="http://c.biancheng.net/python/" id="link1">python教程</a>,
# <a href="http://c.biancheng.net/c/" id="link2">c语言教程</a> and
# """
# soup = BeautifulSoup(html_doc, 'html.parser')
# body_tag = soup.body
# print(body_tag)
# print(body_tag.contents)
# for child in body_tag.children:
#     print(child)

# html_doc = """
# <html><head><title>"c语言中文网"</title></head>
# <body>
# <p class="title"><b>c.biancheng.net</b></p>
# <p class="website">一个学习编程的网站</p>
# <a href="http://c.biancheng.net/python/" id="link1">python教程</a>
# <a href="http://c.biancheng.net/c/" id="link2">c语言教程</a>
# <a href="http://c.biancheng.net/django/" id="link3">django教程</a>
# <p class="vip">加入我们阅读所有教程</p>
# <a href="http://vip.biancheng.net/?from=index" id="link4">成为vip</a>
# """
# soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.find_all("a"))
# print(soup.find_all("a", limit=2))
# print(soup.find_all("p", class_="website"))
# print(soup.find_all(id="link4"))
# print(soup.find_all(["b", "a"]))
# print(soup.find_all("a", id=re.compile(r'.\d')))
# print(soup.find_all(id=True))
# for tag in soup.find_all(True):
#     print(tag.name, end=" ")
# for tag in soup.find_all(re.compile("b")):
#     print(tag.name)
# print(soup("a"))


# html_doc = """
# <html><head><title>"c语言中文网"</title></head>
# <body>
# <p class="title"><b>c.biancheng.net</b></p>
# <p class="website">一个学习编程的网站</p>
# <a href="http://c.biancheng.net/python/" id="link1">python教程</a>
# <a href="http://c.biancheng.net/c/" id="link2">c语言教程</a>
# <a href="http://c.biancheng.net/django/" id="link3">django教程</a>
# <p class="vip">加入我们阅读所有教程</p>
# <a href="http://vip.biancheng.net/?from=index" id="link4">成为vip</a>
# """
# soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.find("a"))
# print(soup.find("title"))
# print(soup.find("a", href="http://c.biancheng.net/python/"))
# print(soup.find(class_=re.compile("tit")))
# print(soup.find(attrs={"class": "vip"}))
# print(soup.find("bdi"))
# print(soup.find_all("audio"))
# print(soup.head.title)
# print(soup.find("head").find("title"))
# print(soup.find("head").find_all("title"))

html_doc = """
<html><head><title>"c语言中文网"</title></head>
<body>
<p class="title"><b>c.biancheng.net</b></p>
<p class="website">一个学习编程的网站</p>
<a href="http://c.biancheng.net/python/" id="link1">python教程</a>
<a href="http://c.biancheng.net/c/" id="link2">c语言教程</a>
<a href="http://c.biancheng.net/django/" id="link3">django教程</a>
<p class="vip">加入我们阅读所有教程</p>
<a href="http://vip.biancheng.net/?from=index" id="link4">成为vip</a>
<p class="introduce">介绍:
<a href="http://c.biancheng.net/view/8066.html" id="link5">关于网站</a>
<a href="http://c.biancheng.net/view/8092.html" id="link6">关于站长</a>
</p>
"""
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.select("title"))
print(soup.select("a[href]"))
print(soup.select(".vip"))
print(soup.select("html head title"))
print(soup.select("p + a"))
print(soup.select("p ~ #link3"))
print(soup.select("p ~ a:nth-of-type(1)"))
print(soup.select("p > a"))
print(soup.select(".introduce > #link5"))