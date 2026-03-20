# import time
#
# from selenium import webdriver
# from selenium.common import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.wait import WebDriverWait
#
#
# browser = webdriver.Chrome()
# browser.maximize_window()  # 务必最大化，防止布局变为移动端模式
#
# try:
#     print("正在访问百度...")
#     browser.get("https://www.baidu.com")
#
#     # 【修改1】将等待时间从 10秒 延长到 30秒，应对网络慢的情况
#     wait = WebDriverWait(browser, 30)
#
#     print("等待搜索框加载...")
#     # 尝试寻找输入框
#     input_item = wait.until(ec.visibility_of_element_located((By.ID, "chat-textarea")))
#
#     print("搜索框已找到，正在输入...")
#     input_item.send_keys("Python")
#     input_item.send_keys(Keys.ENTER)
#
#     # 等待结果
#     wait.until(ec.presence_of_element_located((By.ID, "content_left")))
#
#     print("当前URL:", browser.current_url)
#     print("操作成功！")
#
# except TimeoutException:
#     print("\n========= 发生错误：找不到元素 =========")
#     print("当前浏览器所在的 URL 是:", browser.current_url)
#     print("可能原因：1.网速太慢 2.弹出了验证码 3.页面加载失败")
#
#     # 【修改2】报错时自动截图，保存到当前目录下，帮你看清当时浏览器里显示了什么
#     browser.save_screenshot("debug_error.png")
#     print("已保存截图到项目目录下的 debug_error.png，请打开查看！")
#
#     # 打印一部分网页源码看看是不是被拦截了
#     print("网页源码前500个字符:", browser.page_source[:500])
#
# except Exception as e:
#     print(f"发生了其他错误: {e}")
#
# finally:
#     # 停留几秒让你肉眼观察一下浏览器窗口
#     time.sleep(5)
#     browser.quit()
import datetime
import re
from encodings import unicode_escape

import requests
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser = webdriver.Firefox()
# browser = webdriver.Edge()
# browser = webdriver.PhantomJS()
# browser = webdriver.Safari()


# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# print(browser.page_source)
# browser.quit()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# input_first = browser.find_element(By.ID, "q")
# input_second = browser.find_element(By.CSS_SELECTOR, "#q")
# input_third = browser.find_element(By.XPATH, "//*[@id='q']")
# print(input_first)
# print(input_second)
# print(input_third)
# browser.close()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# lst = browser.find_elements(By.CSS_SELECTOR, "div li")
# print(lst)
# browser.close()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# input_item = browser.find_element(By.ID, "q")
# input_item.send_keys("iPhone")
# time.sleep(1)
# input_item.clear()
# input_item.send_keys("iPad")
# button = browser.find_element(By.CLASS_NAME, "btn-search")
#
# button.click()
# browser.close()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver import ActionChains
# browser = webdriver.Chrome()
# url = "http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
# browser.get(url)
# browser.switch_to.frame("iframeResult")
# source = browser.find_element(By.CSS_SELECTOR, "#draggable")
# target = browser.find_element(By.CSS_SELECTOR, "#droppable")
# actions = ActionChains(browser)
# actions.drag_and_drop(source, target)
# actions.perform()


# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("https://www.zhihu.com/explore")
# browser.execute_script('alert("To Bottom")')


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# logo = browser.find_element(By.ID, 'Popover1-toggle')
# print(logo)
# print(logo.get_attribute("class"))


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# input = browser.find_element(By.CLASS_NAME, 'i7cW1UcwT6ThdhTakqFm')
# print(input)
# print(input.id)
# print(input.size)
# print(input.location)
# print(input.tag_name)
# print(input.text)


# import time
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# browser = webdriver.Chrome()
# url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)
# browser.switch_to.frame('iframeResult')
# try:
#     logo = browser.find_element(By.CLASS_NAME, 'logo')
# except NoSuchElementException:
#     print("NO LOGO")
# browser.switch_to.parent_frame()
# logo = browser.find_element(By.CLASS_NAME, 'logo')
# print(logo)
# print(logo.text)


# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# browser.implicitly_wait(10)
# browser.get("http://www.zhihu.com/explore")
# input = browser.find_element(By.CLASS_NAME, "i7cW1UcwT6ThdhTakqFm")
# print(input)


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# browser = webdriver.Chrome()
# browser.get("https://www.taobao.com")
# wait = WebDriverWait(browser, 10)
# input = wait.until(EC.presence_of_element_located((By.ID, "q")))
# button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-search")))
# print(input)
# print(button)


# import time
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("https://www.baidu.com/")
# browser.get("https://www.taobao.com/")
# browser.get("https://www.zhihu.com/")
# browser.back()
# time.sleep(1)
# browser.forward()
# browser.close()


# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("https://www.zhihu.com/explore")
# print(browser.get_cookies())
# browser.add_cookie({
#     "name": "zhihu",
#     "domain": "www.zhihu.com",
#     "value": "germey",
# })
# print(browser.get_cookies())
# browser.delete_all_cookies()
# print(browser.get_cookies())


# import time
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("https://www.baidu.com")
# browser.execute_script("window.open()")
# print(browser.window_handles)
#
# browser.switch_to.window(browser.window_handles[1])
# browser.get("https://www.taobao.com")
# time.sleep(10)
#
# browser.switch_to.window(browser.window_handles[0])
# browser.get("https://python.org")


# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# try:
#     browser.get("https://www.baidu.com")
# except TimeoutException:
#     print("TimeoutException")
#
#
# try:
#     browser.find_element(By.ID, "hello")
# except NoSuchElementException:
#     print("NoSuchElementException")
# finally:
#     print("finally")
#     browser.close()


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.wait import WebDriverWait
# import random
# import logging
#
#
# def selenium_screenshot(url, css_element: str, width, height):
#     ua = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101Firefox/50.0"
#     driver = ""
#     ip = "xxx.xxx.xxx.xxx"
#     try:
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("user-agent={}".format(ua))
#         chrome_options.add_argument(f"--proxy-server=http://{ip}:port")
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.maximize_window()
#         if width:
#             driver.set_window_size(width, height)
#         driver.get(url)
#         wait = WebDriverWait(driver, 10)
#         wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_element)))
#         ele = driver.find_element(By.CSS_SELECTOR, css_element)
#     except Exception as err:
#         logging.warning(f"{url} selenium_screenshot false: {err}")
#         return
#     else:
#         save_file_path = f"{random.random()}.png"
#         ele.screenshot(save_file_path)
#         logging.info(f"selenium_screenshot success: {url}")
#         return save_file_path
#     finally:
#         if driver:
#             driver.quit()
#
#
# selenium_screenshot("https://www.taobao.com", ".search-suggest-combobox-imageSearch-input", 100, 100)


# from lxml import etree
# text = "<h1>hda</h1>"
# html = etree.HTML(text)
# result = html.xpath("//h1")
# print(html.xpath("//h1")[0].text)
# print(result[0].text)


# from lxml import etree
# text = """
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a>
#      </ul>
#  </div>
# """
# html = etree.HTML(text)
# result = etree.tostring(html)
# print(result)
# result = html.xpath("//li")
# print(result)
# print(result[0])
# result = html.xpath("//li/a")
# print(result)
# result = html.xpath("//li/a")
# print(result)
# result = html.xpath("//a[@href='link4.html']/../@class")
# print(result)
# result = html.xpath("//li[@class='item-0']")
# print(result)
# result = html.xpath("//li[@class='item-0']/a/text()")
# print(result)
# result = html.xpath("//li[@class='item-0']//text()")
# print(result)
# result = html.xpath("//li/a/@href")
# print(result)


# from lxml import etree
# text = """
# <li class="li li-first"><a href="link.html">first item</a></li>
# """
# html = etree.HTML(text)
# resutl = html.xpath("//li[contains(@class,'li')]/a/text()")
# print(resutl)


# from lxml import etree
# text = """
# <li class="li li-first" name="item"><a href="link.html">first item</a></li>
# """
# html = etree.HTML(text)
# result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
# print(result)
# print(result)


# from lxml import etree
# text = """
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a>
#      </ul>
#  </div>
# """
# html = etree.HTML(text)
# result = html.xpath('//li[1]/a/text()')
# print(result)
# result = html.xpath('//li[last()]/a/text()')
# print(result)
# result = html.xpath('//li[position()<3]/a/text()')
# print(result)
# result = html.xpath('//li[last()-2]/a/text()')
# print(result)


# from lxml import etree
# text = """
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html"><span>first item</span></a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a>
#      </ul>
#  </div>
# """
# html = etree.HTML(text)
# result = html.xpath('//li[1]/ancestor::*')
# print(result)
# result = html.xpath('//li[1]/ancestor::div')
# print(result)
# result = html.xpath('//li[1]/attribute::*')
# print(result)
# result = html.xpath('//li[1]/child::a[@href="link1.html"]')
# print(result)
# result = html.xpath('//li[1]/descendant::span')
# print(result)
# result = html.xpath('//li[1]/following::*[2]')
# print(result)
# result = html.xpath('//li[1]/following-sibling::*')
# print(result)


# from bs4 import BeautifulSoup
# html = """
# <html>
#     <head><title>The Dormouse's story</title></head>
# <body>
#     <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
#     <p class="story">Once upon a time there were three little sisters; and their names were
#         <a href="http://example.com/elsie" class="sister" id="link1 link4"><span>Elsie</span></a>
#         Hello
#         <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
#         and
#         <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
#         and they lived at the bottom of a well.
#     </p>
#     <p class="story">...</p>
# """
# soup = BeautifulSoup(html, "lxml")
# print(soup.prettify())
# print(soup.title)
# print(type(soup.title))
# print(soup.title.string)
# print(soup.title.name)
# print(soup.p.attrs)
# print(soup.p['class'])
# print(soup.p["name"])
# print(soup.p.contents)
# print(soup.p.children)
# for i, child in enumerate(soup.p.children):
#     print(i, child)
# print(soup.p.descendants)
# for i, child in enumerate(soup.p.descendants):
#     print(i, child)
# print(soup.a.parent)
# print(soup.a.parents)
# print(list(enumerate(soup.a.parents)))
# print('Next sibing', soup.a.next_sibling)
# print('Prev sibing', soup.a.previous_sibling)
# print('Next siblings', list(enumerate(soup.a.next_sibling)))
# print('Prev siblings', list(enumerate(soup.a.previous_sibling)))


# from bs4 import BeautifulSoup
# import re
# html  = """
# <div class="panel">
# <div class="panel-heading">
# <h4>Hello</h4>
# </div>
# <div class="panel-body">
# <ul class="list" id="list-1" name="elements">
# <li class="element">Foo</li>
# <li class="element">Bar</li>
# <a> Hello, this is a link</a>
# <a> Hello, this is a link, too</a>
# </ul>
# <ul class="list list-small" id="list-2">
# <li class="element">Foo</li>
# <li class="element">Bar</li>
# </ul>
# </div>
# </div>
# """
# soup = BeautifulSoup(html, "lxml")
# print(1, soup.find_all('ul'))
# print(2, type(soup.find_all('ul')[0]))
# for ul in soup.find_all('ul'):
#     print(ul.find_all("li"))
#     for li in ul.find_all("li"):
#         print(li.string)
# print(3, soup.find_all(attrs={"id": "list-1"}))
# print(4, soup.find_all(id='list-1'))
# print(5, soup.find_all(attrs={"name": "elements"}))
# print(6, soup.find_all(class_="element"))
# print(7, soup.find_all('li', {'class': 'element'}))
# print(8, soup.find_all(string=re.compile("link")))
# print(9, soup.find('ul'))
# print(10, soup.find(class_="list"))


# from bs4 import BeautifulSoup
# html = """
# <div class="panel">
# <div class="panel-heading">
# <h4>Hello</h4>
# </div>
# <div class="panel-body">
# <ul class="list" id="list-1" name="elements">
# <li class="element">Foo</li>
# <li class="element">Bar</li>
# <a> Hello, this is a link</a>
# <a> Hello, this is a link, too</a>
# </ul>
# <ul class="list list-small" id="list-2">
# <li class="element">Foo</li>
# <li class="element">Bar</li>
# </ul>
# </div>
# </div>
# """
# soup = BeautifulSoup(html, "lxml")
# print(soup.select('.panel .panel-heading'))
# print(soup.select('ul li'))
# print(soup.select('#list-2 .element'))
# print(type(soup.select('ul')[0]))
# for ul in soup.select('ul'):
#     print(ul['id'])
#     print(ul.select('li'))
# for li in soup.select('li'):
#     print('Get TEXT', li.get_text())
#     print('String:', li.string)


# from pyquery import PyQuery as pq
# html = """
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
# """
# # doc = pq(html)
# # print(doc("li"))
#
# doc = pq(url="https://cuiqingcai.com")
# print(doc("title"))
#
# doc = pq(filename="demo.html")
# print(doc("li"))


# from pyquery import PyQuery as pq
# html = """
# <div id="container">
#     <ul class="list">
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
# """
# doc = pq(html)
# print(doc('#container .list li'))
# print(type(doc('#container .list li')))


# from pyquery import PyQuery as pq
# html = """
# <div class='wrap'>
# <div id="container">
#     <ul class="list">
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-0 active"><a href="link3.html">third item</a></li>
#          <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
#  </div>
# """
# doc = pq(html)
# items = doc('.list')
# print(type(items))
# print(items)
#
# lst = items.find('li')
# print(type(lst))
# print(lst)
#
# lst = items.children('.active')
# print(lst)
#
# container = items.parent()
# print(type(container))
# print(container)
#
# parents = items.parent()
# print(type(parents))
# print(parents)
#
# parent = items.parents('.wrap')
# print(type(parent))
# print(parent)
#
# li = doc('.list .item-0.active')
# print(li.siblings())
# print(li.siblings('.active'))


# from pyquery import PyQuery as pq
# html = """
# <div class='wrap'>
# <div id="container">
#     <ul class="list">
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-0 active"><a href="link3.html">third item</a></li>
#          <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
#  </div>
# """
# doc = pq(html)
# li = doc('.item-0.active')
# print(li)
# print(str(li))
#
# lst = doc('li').items()
# print(type(lst))
# for li in lst:
#     print(li, type(li))
#
# a = doc('.item-0.active a')
# print(a, type(a))
# print(a.text())
# print(a.html())
# print(a.attr('href'))
#
# a = doc('a')
# for item in a.items():
#     print(item.attr('href'))


# from pyquery import PyQuery as pq
# html = """
# <div class='wrap'>
# <div id="container">
#     <ul class="list">
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-0 active"><a href="link3.html">third item</a></li>
#          <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
#  </div>
# """
# doc = pq(html)
# li = doc('.item-0.active')
# print(li)
# li.removeClass('active')
# print(li)
# li.addClass('active')
# print(li)
# li.attr('name', 'link')
# print(li)
# li.text('changed item')
# print(li)
# li.html('<apan>changed item</span>')
# print(li)
#
# html = """
# <div class="wrap">
#     Hello,World
# <p>This is a paragraph.</p>
# </div>
# """
# doc = pq(html)
# wrap = doc('.wrap')
# print(wrap.text())
# wrap.find('p').remove()
# print(wrap.text())


# from pyquery import PyQuery as pq
# html = """
# <div class='wrap'>
# <div id="container">
#     <ul class="list">
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-0 active"><a href="link3.html">third item</a></li>
#          <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
#  </div>
# """
# doc = pq(html)
# # li = doc('li:first-child')
# # print(li)
# #
# # li = doc('li:last-child')
# # print(li)
# #
# # li = doc('li:nth-child(2)')
# # print(li)
#
# li = doc('li:gt(2)')
# print(li)
#
# li = doc('li:nth-child(2n)')
# print(li)
#
# li = doc('li:contains(second)')
# print(li)


# file = open('explore.txt', 'a', encoding="utf-8")
# file.write('\n'.join(["question", "author", "answer"]))
# file.write('\n' + '=' * 50 + '\n')
# file.close()


# import json
# with open('data.json', "r") as file:
#     text = file.read()
#     data = json.loads(text)
#     print(data)


# import json
# str_ = """
# [{
#     "name":"Bob",
#     "gender":"male",
#     "birthday":"1992-10-18"
# },{
#     "name":"Selina",
#     "gender":"female",
#     "birthday":"1995-10-18"
# }]
# """
# print(type(str_))
# data = json.loads(str_)
# print(type(data))
# print(data)


# import json
# data =  [{
#     "name": "Bob",
#     "gender": "male",
#     "birthday": "1992-10-18"
# }]
# with open('data.json', 'w') as fi:
#     fi.write(json.dumps(data, indent=2))


# import json
# data = [{
#     "name": "王二",
#     "gender": "男",
#     "birthday": "1992-10-18"
# }]
# with open('data.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(data, indent=2, ensure_ascii=False))


# import csv
# with open('data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ')
#     writer.writerow(['id', 'name', 'age'])
#     writer.writerow(['10001', 'Mike', '20'])
#     writer.writerow(['10002', 'Bob', '22'])
#     writer.writerow(['10003', 'Jordan', '21'])


# import csv
# with open('data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['id', 'name', 'age'])
#     writer.writerows([['10001', 'Mike', '20'], ['10002', 'Bob', '22'], ['10003', 'Jordan', '21']])


# import csv
# with open('data.csv', "w", encoding='utf-8', newline='') as csvfile:
#     filename = ['id', 'name', 'age']
#     writer = csv.DictWriter(csvfile, fieldnames=filename)
#     writer.writeheader()
#     writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})
#     writer.writerow({'id': '10002', 'name': 'Bob', 'age': 22})
#     writer.writerow({'id': '10004', 'name': '王伟', 'age': 20})


# import csv
# with open('data.csv', 'r', encoding="utf-8") as rf:
#     reader = csv.DictReader(rf, fieldnames=("id", "name", "age"))
#     for i in reader:
#         print(dict(i))


# import pymysql
# db = pymysql.connect(
#     host='localhost',        # 本机运行一定要用 localhost
#     port=3306,               # 对应 docker ps 中显示的外部端口
#     user='root',             # 你的 MYSQL_USER
#     password='rootpassword',     # 你的 MYSQL_PASSWORD
#     database='my_database',   # 你的 MYSQL_DATABASE
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )
# # db = pymysql.connect(host="localhost", user="user", password="password", port=3306)
# cursor = db.cursor()
# cursor.execute("select version();")
# data = cursor.fetchone()
# print('Database version : ', data)

# cursor.execute('create database spiders default charset utf8;')
# db.close()


# import pymysql
# db = pymysql.connect(host='localhost', user='root', password='rootpassword', port=3306, db='spiders')
# cursor = db.cursor()
# sql = "create table if not exists students(id varchar(255) not null,name varchar(255) not null,age int not null,primary key(id))"
# cursor.execute(sql)
# db.close()


# import pymysql
# db = pymysql.connect(host='localhost', user='root', password='rootpassword', port=3306, db='spiders')
# cursor = db.cursor()
# data = {
#     'id': '20291003',
#     'name': 'Bob',
#     'age': 22
# }
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s']*len(data))
# sql = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys, values=values)
# print(sql)
# try:
#     if cursor.execute(sql, tuple(data.values())):
#         print("Successful")
#         db.commit()
# except:
#     print("Failed")
#     db.rollback()
# finally:
#     db.close()


# import pymysql
# db = pymysql.connect(host='localhost', user='root', password='rootpassword', port=3306, db='spiders')
# cursor = db.cursor()
# data = {
#     'id': '20291001',
#     'name': 'Bob',
#     'age': 21
# }
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s']*len(data))
# sql = 'insert into {table} ({keys}) values ({values}) on duplicate key update'.format(
#     table=table,
#     keys=keys,
#     values=values
# )
# print(sql)
# update = ','.join(" {key} = %s".format(key=key) for key in data.keys())
# sql += update
# print(sql)
# try:
#     cursor.execute(sql, tuple(data.values())*2)
#     print('success')
#     db.commit()
# except Exception as e:
#     print(e)
#     db.rollback()
# finally:
#     db.close()


# import pymysql
# db = pymysql.connect(host='localhost', user='root', password='rootpassword', port=3306, db='spiders')
# cursor = db.cursor()
# table = 'students'
# condition = 'age>20'
# sql = 'delete from {table} where {condition}'.format(table=table, condition=condition)
# try:
#     cursor.execute(sql)
#     db.commit()
# except Exception as e:
#     db.rollback()
#     print(e)
# finally:
#     db.close()


# import pymysql
# db = pymysql.connect(host='localhost', user='root', password='rootpassword', port=3306, db='spiders')
# cursor = db.cursor()
# sql = 'select * from students where age>20'
# try:
#     cursor.execute(sql)
#     print('Count:', cursor.rowcount)
#     one = cursor.fetchone()
#     print('one:', one)
#     results = cursor.fetchall()
#     print('results:', results)
#     print('Results type:', type(results))
#     for row in results:
#         print(row)
# except Exception as e:
#     print(e)
# finally:
#     cursor.close()
#     db.close()


# import requests
# import logging
#
#
# def main():
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
#     for retry_time in range(3):
#         proxy = requests.get("http://localhost:5555/random").text.strip()
#         print('get random proxy', proxy)
#         proxies = {'http': f'http://{proxy}'}
#         try:
#             html = requests.get('https://httpbin.org/', proxies=proxies, headers=headers, timeout=5)
#             print(html.status_code, html.text)
#             break
#         except Exception as e:
#             logging.error(e)
#
#
# if __name__ == '__main__':
#     main()


# import requests
# import logging
#
# def main():
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
#     for retry_times in range(3):
#         proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
#         print('get random proxy', proxy)
#         proxies = {"http": f'http://{proxy}'}
#         try:
#             html = requests.get('https://httpbin.org/', proxies=proxies, headers=headers)
#             print(html.status_code, html.text)
#             break
#         except Exception as e:
#             logging.error(e)
#
#
# if __name__ == '__main__':
#     main()


# import requests
#
# proxy = "60.188.5.136:80"
# proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
# socks_proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}
# try:
#     response = requests.get("http://httpbin.org/", proxies=proxies)
#     print(response.json()["origin"])
# except Exception as e:
#     print(e)


# import requests
# import socks
# import socket
#
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
# for retry_times in range(3):
#     proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
#     print(proxy)
#
# socks.set_default_proxy(socks.SOCKS5, proxy.split(":")[0], int(proxy.split(":")[1]))
# socket.socket = socks.socksocket
# try:
#     response = requests.get('http://httpbin.org/')
#     print(response.json()["origin"])
# except Exception as e:
#     print(e)


# import requests
# import httpx
#
#
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
# proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
# print(proxy)
# proxies = {"http": "http://" + proxy}
# with httpx.Client(proxy=proxy) as client:
#     response = client.get("http://httpbin.org/")
#     print(response.json()["origin"])


# import requests
# import asyncio
# import aiohttp
#
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
# proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get("http://httpbin.org/", headers=headers) as resp:
#             print(await resp.text())
#
#
# asyncio.run(main())



# import requests
# import asyncio
# import aiohttp
# from pyppeteer import launch
#
# async def main():
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
#     proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
#     print(proxy)
#     browser = await launch({"args": [f'--proxy-server=http://{proxy}'], "headless": False})
#     page = await browser.newPage()
#     await page.goto("http://httpbin.org/")
#     print(await page.content())
#     await browser.close()
#
# asyncio.get_event_loop().run_until_complete(main())


# import requests
# from playwright.sync_api import sync_playwright
#
# proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
# with sync_playwright() as playwright:
#     browser = playwright.chromium.launch(headless=False, proxy=proxy)
#     page = browser.new_page()
#     page.goto("http://httpbin.org/")
#     print(page.content())
#     browser.close()


# from redis import StrictRedis
#
# redis = StrictRedis(host='localhost', port=6379, db=0, password=None)
# redis.set('name', 'Bob')
# print(redis.get('name'))


# from redis import StrictRedis
# redis = StrictRedis(host='localhost', port=6379, db=0, password=None)
# redis.set('name', 'Bob')
# redis.set('name1', 'Bob1')
# redis.set('name2', 'Bob2')
# redis.set('name3', 'Bob3')
#
# redis.exists('name')
# redis.expire('name', 10)
# redis.ttl('name')
# redis.delete('name3')
# redis.dbsize()
#
# redis.type('name')
# redis.move('name1', 2)
# redis.rename('name2', 'nickname')
# redis.keys('n*')
#
# redis.randomkey()
# # redis.flushdb()
# # redis.flushall()


# from redis import StrictRedis
# redis = StrictRedis(host='localhost', port=6379, db=0)
# redis.set('name', 'Bob')
# redis.get('name')
# print(redis.get('name'))
# redis.setex('name', 1, "James")
# redis.incr('count', 1)
# redis.decr('age',1)
# redis.mset({'name1': 'Durant', 'name2': 'James'})
# redis.mget(['name', 'nickname'])
# redis.getset('name', "Mike")
# redis.setnx('newname', 'James')
# redis.msetnx({'name3': 'Smith', 'name4': 'Curry'})
# redis.setrange('name', 6, 'World')
# redis.append('nickname', 'ok')
# redis.substr('name', 1, 4)
# redis.getrange('name', 1, 4)
# print(redis.getrange('name', 1, 4))


# from redis import StrictRedis
# r = StrictRedis(host='localhost', port=6379, db=0)
# url = 'https://www.baidu.com'
# url1 = 'https://www.taobao.com'
# url2 = 'https://www.sina.com.cn'
# r.rpush('list', url, url1, url2)
# for i in range(r.llen('list')):
#     t = r.lindex('list', i)
#     item = t.decode('utf8')
#     print(item)
#
# r.rpush('list', url)
# r.lpush('list', url)
# r.rpop('list', url)
# r.lpop('list', url)
# r.lrange('list', 0, -1)
# r.lrange('list', 0, 2)
# r.lrem('list', 2, url)
# r.lrem('list', -2, url)
# r.lrem('list', 0, url)
# r.llen('list')
# r.lindex('list', 1)


# from redis import StrictRedis
# r = StrictRedis(host='localhost', port=6379, db=0)
# r.sadd('tags', 'Book', 'Tea', 'Coffee')
# for me in r.smembers('tags'):
#     item = me.decode('utf-8')
#     print(item)
# r.sadd("tags", "Book")
# r.smembers("tags", "Book")
# r.srem("tags", "Book")
# r.scard('tags')
# r.smembers('tags')


# from redis import StrictRedis
# r = StrictRedis(host='localhost', port=6379, db=0)
# r.hset("price", "cake", 1)
# r.hget("price", "cake")
# r.hgetall("price")
# r.hmset("price", {"banana": 2, "pear": 3})
# r.hkeys("price")
# r.hvals("price")
# r.hdel("price", "cake")
# r.hexists("price", "cake")
# print(r.hlen("price"))


# import random
# import redis
#
#
# class RedisClient(object):
#     def __init__(self, _type, website, host='localhost', port=6379,password=None):
#         self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
#         self.type = _type
#         self.website = website
#
#     def name(self):
#         return f"{self.type}:{self.website}"
#
#     def set(self, username, value):
#         return self.db.hset(self.name(), username, value)
#
#     def get(self, usernma):
#         return self.db.hget(self.name(), usernma)
#
#     def delete(self, username):
#         return self.db.hdel(self.name(), username)
#
#     def count(self):
#         return self.db.hlen(self.name())
#
#     def random(self):
#         return self.db.hkeys(self.name())
#
#     def username(self):
#         return self.db.hkeys(self.name())
#
#     def all(self):
#         return self.db.hgetall(self.name())


# from redis import StrictRedis
#
# def connect_redis(config: dict, db_index: int = 0):
#     _db = StrictRedis(
#         host=config['redis']['host'],
#         port=config['redis']['port'],
#         password=config['auth'],
#         db=db_index
#     )
#     return _db
#
# local_config = {
#     "host": "localhost",
#     "port": 6379,
#     "auth": None,
#     "db": 0
# }
#
# redis_db = connect_redis(local_config, db_index=0)


from redis import StrictRedis
# import json
#
# def save_redis_record(redis_db, key_name, record):
#     redis_db.lpush(key_name, json.dumps(record, ensure_ascii=False))
#     redis_db.rpush(key_name, json.dumps(record, ensure_ascii=False))
#
#
# def fetch_redis_record(redis_db, key_name):
#     data1 = json.loads(redis_db.lpop(key_name))
#     data2 = json.loads(redis_db.rpop(key_name))
#
#
# def read_range_redis_record(redis_db, key_name, s_index, e_index):
#     reocrds = redis_db.lrange(key_name, s_index, e_index)
#     for record in reocrds:
#         print(json.loads(record))


# import requests
# from lxml import etree
# headers = {
#     'Host': "github.com",
#     'Referer': "https://github.com/login?return_to=%2Fjoin",
#     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36"
# }
# session = requests.Session()
# login_url = "https://github.com/login"
# response = session.get(login_url, headers=headers)
# selector = etree.HTML(response.text)
# token = selector.xpath('//input[@id="login_field"]/@value')
# print(token)


# import threading
# def action(max):
#     for i in range(max):
#         print(threading.current_thread().getName() + " " + str(i))
#
# for i in range(10):
#     print(threading.current_thread().getName() + " " + str(i))
#     if i == 8:
#         t1 = threading.Thread(target=action, args=(10,))
#         # t1.start()
#         # t1.join()
#
#         t2 = threading.Thread(target=action, args=(20,))
#         # t2.start()
#         # t2.join()
#         t2.start()
#         t2.join()
#         t1.start()
#         t1.join()


# import threading
#
# class FKThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.i = 0
#
#     def run(self):
#         while self.i<50:
#             print(threading.current_thread().getName() + " " + str(self.i))
#             self.i += 1
#
# for i in range(100):
#     print(threading.current_thread().getName() + " " + str(i))
#     if i == 20:
#         ft1 = FKThread()
#         ft1.start()
#
#         ft2 = FKThread()
#         ft2.start()
#
# print("Main thread finished")
# ft1.join()
# ft2.join()


# import random
# num = random.randint(1, 10)
# print(num)

# import random
# num = random.random()
# print(num)

# import random
# num = random.uniform(1, 5.3)
# print(num)

# import random
# num1 = random.sample("tomorrow", 6)
# num2 = random.sample([1, 5, 9, "hello", ("hh", 2)], 3)
# num3 = random.sample((2, 8, 36), 2)
# print(num1)
# print(num2)
# print(num3)


# import random
# items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# random.shuffle(items)
# print(items)


# f = open("hello.js")
# try:
#     data = f.read()
#     print(data)
# finally:
#     f.close()
#
# with open("hello.js", "r") as f:
#     data = f.read()
#     print(data)


# class sample:
#     def __enter__(self):
#         print("Run--1:执行enter方法")
#         return self
#
#     def __exit__(self, type1, value, trace):
#         print("Run--3:", type1)
#         print("Run--4:", value)
#         print("Run--5:trace:", trace)
#
#     def execute_action(self):
#         print("Run--6:execute_action")
#         return "无异常"
#
#
# with sample() as file:
#     print('Start')
#     result = file.execute_action()
#     print(result)


# class sample:
#     def __enter__(self):
#         print("Run--1:执行enter方法")
#         return self
#
#     def __exit__(self, type1, value, trace):
#         print("Run--3:", type1)
#         print("Run--4:", value)
#         print("Run--5:trace:", trace)
#
#     @staticmethod
#     def execute_action():
#         print("Run--6:execute_action")
#         return 1/0
#
#
# with sample() as file:
#     print('Start')
#     result = file.execute_action()
#     print(result)


# import asyncio
# async def execute(x):
#     print("Number:", x)
# coroutine = execute(1)
# print("Coroutine:", coroutine)
# print("After calling execute")
# loop = asyncio.get_event_loop()
# loop.run_until_complete(coroutine)
# print("After calling loop")


# import asyncio
# async def execute(x):
#     print("Number:", x)
#     return x
#
# coroutine = execute(1)
# print("Coroutine:", coroutine)
# print("After calling execute")
# loop = asyncio.get_event_loop()
# task = loop.create_task(coroutine)
# print("Task:", task)
# loop.run_until_complete(task)
# print("Task:", task)
# print("After calling loop")


# import asyncio
# async def execute(x):
#     print("Number:", x)
#     return x
#
# coroutine = execute(1)
# task = asyncio.ensure_future(coroutine)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(task)
# print("Task:", task)


# import asyncio
# import requests
# async def request():
#     url = 'https://www.baidu.com'
#     status = requests.get(url)
#     return status
#
# def callback(task):
#     print(f"Status: {task.result()}")
#
# coroutine = request()
# task = asyncio.ensure_future(coroutine)
# task.add_done_callback(callback)
# print("Task: ", task)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(task)
# print("Task: ", task)


# import asyncio
# import requests
# async def request():
#     url = "https://www.baidu.com"
#     status = requests.get(url)
#     return status
#
# coroutine = request()
# task = asyncio.ensure_future(coroutine)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(task)
# print(task)
# print(task.result())


# import asyncio
# import requests
# async def request():
#     url = "https://www.baidu.com"
#     status =  requests.get(url)
#     return status
#
# tasks = [asyncio.ensure_future(request()) for _ in range(10)]
# print(tasks)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
# for task in tasks:
#     print(task.result())


# import asyncio
# import requests
# import time
# start = time.time()
# async def get(url):
#     return requests.get(url)
# async def request():
#     url = "https://www.baidu.com"
#     print("Waiting for", url)
#     response = await get(url)
#     print(f"Get reponse from {url}, Result: {response.status_code}")
#
# tasks = [asyncio.ensure_future(request()) for _ in range(10)]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
# end = time.time()
# print(f"Total time: {end - start}")


# import asyncio
# import aiohttp
# import time
# start = time.time()
# async def get(url):
#     session = aiohttp.ClientSession()
#     response = await session.get(url)
#     result = await response.text()
#     await session.close()
#     return result
#
# async def request():
#     url = 'http://www.newsmth.net/nForum/#!mainpage'
#     print(f"Waiting for {url}")
#     result = await get(url)
#     print(f"Get response from {url}, Result: {result}")
#
# tasks = [asyncio.ensure_future(request()) for _ in range(10)]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
# end = time.time()
# print(f"Total time: {end - start}")


# import aiohttp
# import asyncio
#
# async def main():
#     data = {
#         "name": "germey",
#         "age": 18,
#     }
#     timeout = aiohttp.ClientTimeout(total=10)
#     async with aiohttp.ClientSession(timeout=timeout) as session:
#         async with session.post("http://httpbin.org/post", data=data) as resp:
#             print(f"status code: {resp.status}")
#             print(f"headers: {resp.headers}")
#             print(f"body: {await resp.text()}")
#             print(f"bytes: {await resp.read()}")
#             print(f"json: {await resp.json()}")
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())


# import aiohttp
# import asyncio
#
# CONCURRENCY = 5
# URL = "https://www.baidu.com"
# semaphore = asyncio.Semaphore(CONCURRENCY)
# session = None
#
# async def scrape_api():
#     async with semaphore:
#         print(f"Scraping {URL}")
#         async with session.get(URL) as response:
#             await asyncio.sleep(1)
#             return await response.text()
#
# async def main():
#     global session
#     session = aiohttp.ClientSession()
#     scrape_index_tasks = [asyncio.ensure_future(scrape_api()) for _ in range(100)]
#     await asyncio.gather(*scrape_index_tasks)
#
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())


# class A:
#     def __repr__(self):
#         print("A")
#         return "__repr__"
#
# a = A()
# print(a)
#
# class B:
#     def __bool__(self):
#         print("B")
#         return False
#
# b = B()
# print(bool(b))

# class C:
#     def __getattr__(self, name):
#         print(f"__getattr__ {name}")
#
#     def __setattr__(self, name, value):
#         print(f"__setattr__ {name} {value}")
#         super().__setattr__(name, value)
#
#     def __delattr__(self, name):
#         print(f"__delattr__ {name}")
#         return super().__delattr__(name)
#
# c = C()
# c.name
# c.name = "suzhou"
# print(c.name)
# del c.name


# import os
# print(os.path.join("user", "bin", "spam"))
# myFiles = ["accounts.txt", "details.csv", "invite.docx"]
# for filename in myFiles:
#     print(os.path.join("E:\\", filename))


# import os
# print(os.getcwd())
# os.chdir("D:\\")
# print(os.getcwd())
# os.chdir("E:\\project")
# print(os.getcwd())
# os.chdir("D:\\")
# print(os.getcwd())


# import os
# print(os.path.abspath('.'))
# print(os.path.isabs("E:\\projects\\Demo"))
# print(os.path.abspath("E:\\projects"))
# print(os.path.realpath("E:\\projects"))


# import os
# path = "E:\\projects\\Demo\\ip.txt"
# print(os.path.basename(path))
# print(os.path.splitext(path))
# print(os.path.dirname(path))
# print(os.path.split(path))
# print(os.path.split(os.path.sep))


# import os
# # print(os.path.getsize("test.txt"))
# print(os.listdir("."))
# totalsize = 0
# for filename in os.listdir("."):
#     totalsize += os.path.getsize(filename)
# print(totalsize)


# import os
# print(os.path.exists("C:\Users\Administrator\PycharmProjects\Demo"))
# print(os.path.isdir("C:\Users\Administrator\PycharmProjects\Demo"))
# print(os.path.isfile("C:\Users\Administrator\PycharmProjects\Demo"))


# import requests
# url1 = "http://hd.chinatax.gov.cn/fagui/initCredit.jsp"
# session = requests.Session()
# resp1 = session.get(url1)
# print(resp1.text)


# from selenium import webdriver
#
# def driver_chrome_cookie():
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--headless')
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get('http://www.cyicai.com/information/applyForSubscription')
#     cookies = driver.get_cookies()
#     print(cookies)
#     if cookies[0]["name"] == "__jsluid":
#         new_cookies = cookies[0]["name"] + "=" + cookies[0]["value"] + ";" + cookies[1]["name"] + "=" + cookies[1]["value"] + "=" + cookies[1]["value"]
#         print(new_cookies)
#
#
# if __name__ == '__main__':
#     driver_chrome_cookie()


# spam = ["cat", "bat", "rat", "elephant"]
# del spam[2]
# print(spam)


# cat = ["fat", "black", "loud"]
# size, color, disposition = cat
# print(size)
# print(color)
# print(disposition)


# cat = ["fat", "black", "loud"]
# print(cat.index("black"))


# spam = ["cat", "bat", "bat"]
# spam.append("moose")
# spam.insert(1, "chicken")
# print(spam)


# spam = ["cat", "chicken", "bat", "bat", "moose"]
# spam.remove("cat")
#
# print(spam)


# cat = ["fat", "black", "loud"]
# cat.sort()
# print(cat)
# cat.sort(reverse=True)
# print(cat)


# spam = ["a", "z", "A", "z"]
# spam.sort()
# print(spam)
# spam.sort(key=str.lower)
# print(spam)


# name = "zophie"
# name[3] = "t"


# import copy
# spam = ["A", "B", "C", "D"]
# cheese = copy.copy(spam)
# cheese[1] = 42
# print(spam)
# print(cheese)


# grid = [['.', '.', '.', '.', '.', '.'],
#         ['.', '0', '0', '.', '.', '.'],
#         ['0', '0', '0', '0', '.', '.'],
#         ['0', '0', '0', '0', '0', '.'],
#         ['.', '0', '0', '0', '0', '0'],
#         ['0', '0', '0', '0', '0', '.'],
#         ['0', '0', '0', '0', '.', '.'],
#         ['.', '0', '0', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.']]
# for i in range(len(grid[0])):
#     for j in range(len(grid)):
#         if j == len(grid) - 1:
#             print(grid[j][i])
#         else:
#             print(grid[j][i], end='')


# spam = {
#     "color": "red",
#     "ages": 42
# }
# for k in spam.keys():
#     print(k)
#
# for v in spam.values():
#     print(v)
#
# for k, v in spam.items():
#     print(k, v)


# spam = {
#     "color": "red",
#     "ages": 42
# }
#
# print("color" in spam)
# print(spam["color"])
# print(spam["ages"])
# print("red" in spam.values())


# spam = {
#     "color": "red",
#     "ages": 42
# }
# spam.get("color")
# spam.get("color", "green")
# spam.get("name", "mike")
# print(spam)


# spam = {
#     "color": "red",
#     "ages": 42
# }
# spam.setdefault("name", "pooka")
# print(spam)
# spam.setdefault("color", "black")
# print(spam)


# import pprint
# message = "it was a bright cold day in April"
# count = {}
# for ch in message:
#     count.setdefault(ch, 0)
#     count[ch] = count[ch] - 1
# print(count)
# # pprint.pprint(count)


# dic = dict(zip("abc", [1, 2, 3]))
# print(dic)
# dic = dict(zip(["apple", "pen", "color"], ["red", 1, ["red", "green", "blue"]]))
# print(dic)


# dic = {i:2*i for i in range(3)}
# print(dic)


# dic = dict.fromkeys(range(3), "x")
# print(dic)


# the_board = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
#             'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
#             'low-L': ' ', 'low-M': ' ', 'low-R': ' '}
#
# def print_board(the_board):
#     print(the_board['top-L'] + "|" + the_board['top-M'] + "|" + the_board['top-R'])
#     print("-+-+-")
#     print(the_board['mid-L'] + "|" + the_board['mid-M'] + "|" + the_board['mid-R'])
#     print("-+-+-")
#     print(the_board["low-L"] + "|" + the_board["low-M"] + "|" + the_board["low-R"])
#
# turn = "X"
# for i in range(9):
#     print_board(the_board)
#     print("Turn for " + turn + ". Move on which space?")
#     move = input()
#     the_board[move] = turn
#     if turn == "X":
#         turn = "O"
#     else:
#         turn = "X"
#
# print_board(the_board)


# def displat_inventory(inventory):
#     print("Inventory:")
#     item_total = 0
#     for k, v in inventory.items():
#         print(str(v) + " " + str(k))
#         item_total += v
#     print("Total number of items: " + str(item_total))
#
# def add_to_inventory(inventory, added_items):
#     for i in added_items:
#         inventory.setdefault(i, 0)
#         inventory[i] += 1
#
# inv = {
#     "gold coin": 42,
#     "rope": 1
# }
# dragon_loot = ["gold coin", "dagger", "gold coin", "gold coin", "ruby"]
# add_to_inventory(inv, dragon_loot)
# displat_inventory(inv)


# spam = "Hello World"
# print(spam.upper())
# print(spam.lower())
# print("HELLO".isupper())
# print("hello".islower())


# print("hello".isalpha())
# print("hello123".isalnum())
# print("123".isdecimal())
# print(" ".isspace())
# print("This Is Title".istitle())


# print("Hello World".startswith("Hello"))
# print("Hello World".endswith("World"))


# print(",".join(["cats", "rats", "bats"]))
# print("ABC".join(["cats", "rats", "bats"]))
# print("catsABCratsABCbats".split("ABC"))
# print("cats,rats,bats".split(","))


# print("Hello".rjust(10))
# print("Hello".ljust(10))
# print("Hello".rjust(10, "*"))
# print("Hello".ljust(10, "*"))
# print("Hello".rjust(10, "-"))
# print("Hello".ljust(10, "-"))
# print("Hello".center(10, "="))


# spam = " Hello World"
# print(spam.strip())
# print(spam.lstrip())
# print(spam.rstrip())
# spam = 'SpamSpamBaconSpamEggsSpamSpam'
# print(spam.strip("ampS"))


# import pyperclip
# pyperclip.copy("Hello World")
# print(pyperclip.paste())


# table_data = [["apples", "oranges", "cherries", "bananas"],
#               ["Alice", "Bob", "Carol", "David"],
#               ["dogs", "cats", "moose", "goose"]]
#
# def print_table(table_data):
#     def row_width(table2):
#         max_len = 0
#         for item in table2:
#             if len(item) > max_len:
#                 max_len = len(item)
#         return max_len
#     for i in range(len(table_data[0])):
#         for j in range(len(table_data)):
#             print(table_data[j][i].rjust(row_width(table_data[j])), end=" ")
#         print()
#
# print_table(table_data)


# import re
# phone_num_regex = re.compile(r'\d{3}-\d{3}-\d{3}')
# mo = phone_num_regex.search("My number is 415-456-7890")
# print(mo.group())


# import re
# hero_regex = re.compile(r"Batman|Tina Fey")
# mo1 = hero_regex.search("Batman and Tina Fey.")
# print(mo1.group())
#
# mo2 = hero_regex.search("Tina Fey and batman.")
# print(mo2.group())
#
# bat_regex = re.compile(r"Bat(man|mobile|copter|bat)")
# mo = bat_regex.search("Batmobile lost a weel")
# print(mo.group())
# print(mo.group(1))

# b64_pdf = "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SL5iZYBfvmZlSJDEPDDAQu9Y2cBC71nZoEcv3YENevQtKxv06OUEwSbK/PwblOcoPadcJ7O7r2seWrkKZDSfQzlOSW+LZV6eUSa/xV8+DA6CCmVuZHN0cmVhbQplbmRvYmoKNiAwIG9iago8PC9TdWJ0eXBlL1R5cGUwL1R5cGUvRm9udC9CYXNlRm9udC9ZQkhKTVMrQXRraW5zb25IeXBlcmxlZ2libGUtQm9sZC9FbmNvZGluZy9JZGVudGl0eS1IL0Rlc2NlbmRhbnRGb250c1sxOSAwIFJdL1RvVW5pY29kZSAyMCAwIFI+PgplbmRvYmoKNyAwIG9iago8PC9TdWJ0eXBlL0Zvcm0vRmlsdGVyL0ZsYXRlRGVjb2RlL1R5cGUvWE9iamVjdC9NYXRyaXggWzEgMCAwIDEgMCAwXS9Gb3JtVHlwZSAxL1Jlc291cmNlczw8L1Byb2NTZXQgWy9QREYgL1RleHQgL0ltYWdlQiAvSW1hZ2VDIC9JbWFnZUldL1hPYmplY3Q8PC9pbWcyIDggMCBSPj4+Pi9CQm94WzAgMCA2NjYgMjA5XS9MZW5ndGggODQ+PnN0cmVhbQp4nCvkMlAwMrBUyAXSBgo5XGZmZnAaJJ7DlcEVzpXHZahQzmWk4AVUlcVlaKDgyxUda6CQwlXIVagA0QIxBkQn5yroZ+amGym45CsEcoEgAAJlFL8KZW5kc3RyZWFtCmVuZG9iagoxMSAwIG9iago8PC9LaWRzWzEgMCBSXS9UeXBlL1BhZ2VzL0NvdW50IDEvSVRYVCgyLjEuNyk+PgplbmRvYmoKMjEgMCBvYmoKPDwvTmFtZXNbKEpSX1BBR0VfQU5DSE9SXzBfMSkgMTIgMCBSXT4+CmVuZG9iagoyMiAwIG9iago8PC9EZXN0cyAyMSAwIFI+PgplbmRvYmoKMjMgMCBvYmoKPDwvTmFtZXMgMjIgMCBSL1R5cGUvQ2F0YWxvZy9QYWdlcyAxMSAwIFIvVmlld2VyUHJlZmVyZW5jZXM8PC9QcmludFNjYWxpbmcvQXBwRGVmYXVsdD4+Pj4KZW5kb2JqCjI0IDAgb2JqCjw8L01vZERhdGUoRDoyMDI2MDEyODEwNTMyMCswMScwMCcpL0NyZWF0b3IoSmFzcGVyUmVwb3J0cyBcKExhYmVsQm9nZW5BNF9BNk5ld1wpKS9DcmVhdGlvbkRhdGUoRDoyMDI2MDEyODEwNTMyMCswMScwMCcpL1Byb2R1Y2VyKGlUZXh0IDIuMS43IGJ5IDFUM1hUKT4+CmVuZG9iagp4cmVmCjAgMjUKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDIxNzI1IDAwMDAwIG4gCjAwMDAwMjIwNzAgMDAwMDAgbiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAxNTMzIDAwMDAwIG4gCjAwMDAwMzE3MzAgMDAwMDAgbiAKMDAwMDAzNzg5OSAwMDAwMCBuIAowMDAwMDM4MDQ2IDAwMDAwIG4gCjAwMDAwMDQ0ODkgMDAwMDAgbiAKMDAwMDAxOTEzOSAwMDAwMCBuIAowMDAwMDIwMDkzIDAwMDAwIG4gCjAwMDAwMzgzNTQgMDAwMDAgbiAKMDAwMDAyMjAzNCAwMDAwMCBuIAowMDAwMDIyMTU4IDAwMDAwIG4gCjAwMDAwMzAzNzkgMDAwMDAgbiAKMDAwMDAzMDU4MCAwMDAwMCBuIAowMDAwMDMxMTAxIDAwMDAwIG4gCjAwMDAwMzE4ODAgMDAwMDAgbiAKMDAwMDAzNjc0NSAwMDAwMCBuIAowMDAwMDM2OTQzIDAwMDAwIG4gCjAwMDAwMzczODMgMDAwMDAgbiAKMDAwMDAzODQxOCAwMDAwMCBuIAowMDAwMDM4NDc0IDAwMDAwIG4gCjAwMDAwMzg1MDggMDAwMDAgbiAKMDAwMDAzODYxNCAwMDAwMCBuIAp0cmFpbGVyCjw8L0luZm8gMjQgMCBSL0lEIFs8ZTYzY2I1MTEwNjUzMDE4NDkxNGM1MDM3MjI1NDM3MjM+PDc2YWFhNjhiOTE4ODQ2NTEwMTE4Yjg1MjVhYmI3ZjA5Pl0vUm9vdCAyMyAwIFIvU2l6ZSAyNT4+CnN0YXJ0eHJlZgozODc4MwolJUVPRgo="
#
# import base64
# import os
#
#
# def save_b64_to_disk(mps_id, b64_data, save_dir="downloads/"):
#     # 1. 确保目录存在
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#
#     # 2. 构造完整的文件路径
#     file_path = os.path.join(save_dir, f"{mps_id}.pdf")
#
#     # 3. 解码并写入
#     try:
#         # 解码
#         binary_data = base64.b64decode(b64_data)
#
#         # 写入文件 (注意是 'wb' 模式)
#         with open(file_path, 'wb') as f:
#             f.write(binary_data)
#
#         print(f"PDF已生成: {file_path}")
#         return file_path
#
#     except Exception as e:
#         print(f"保存失败: {e}")
#         return None
#
#
# # 调用
# save_b64_to_disk("mps_id", b64_pdf, "C:\\Users\Administrator\PycharmProjects\Demo\save_files")


# import re
# bat_regex = re.compile(r"Bat(wo)?man")
# mo1 = bat_regex.search("The Adventures of Batman")
# print(mo1.group())
#
# mo2 = bat_regex.search("The Adventures of Batwoman")
# print(mo2.group())
#
# phone_regex = re.compile(r"(\d\d\d-)?\d\d\d-\d\d\d\d")
# mo1 = phone_regex.search("My number is 123-456-7890")
# print(mo1.group())
#
# mo2 = phone_regex.search("My number is 123-7890")
# print(mo2.group())
# print(mo2.group(1))


# import re
# bat_regex = re.compile(r'Bat(wo)*man')
# mo1 = bat_regex.search('The adventures of Batman')
# print(mo1.group())
#
# mo2 = bat_regex.search('The adventures of Batwoman')
# print(mo2.group())
#
# mo3 = bat_regex.search('The adventures of Batwowowowowowoman')
# print(mo3.group())


# import re
# bat_regex = re.compile(r'Bat(wo)+man')
# mo1 = bat_regex.search("The adventures of Batman")
# print(mo1)
#
# mo2 = bat_regex.search("The adventures of Batwoman")
# print(mo2.group())
#
# mo3 = bat_regex.search("The adventures of Batwowowowowoman")
# print(mo3.group())


# import re
# ha_regex = re.compile(r'(Ha){3}')
# mo1 = ha_regex.search('HaHaHa')
# print(mo1.group())
#
# mo2 = ha_regex.search('Ha')
# print(mo2)


# import re
# greedy_ha_regex = re.compile(r'(Ha){3,5}')
# mo1 = greedy_ha_regex.search('HaHaHaHaHa')
# print(mo1.group())

# non_greedy_ha_regex = re.compile(r'(Ha){3,5}?')
# mo2 = non_greedy_ha_regex.search('HaHaHaHaHa')
# print(mo2.group())


# import re
# phone_num_regex = re.compile(r"\d{3}-\d{4}-\d{4}")
# mo = phone_num_regex.findall("Cell:415-5555-9999 Work:222-5554-0000")
# print(mo)
#
# phone_num_regex = re.compile(r"(\d{3})-(\d{3})-(\d\d\d\d)")
# mo = phone_num_regex.findall("Cell:415-555-9999 Work:222-555-0000")
# print(mo)


# import re
# vowel_regex = re.compile(r'[aeiouAEIOU]')
# print(vowel_regex.findall('RoboCop eats baby food. BABY FOOD'))
#
# vowel_regex = re.compile(r'[^aeiouAEIOU]')
# print(vowel_regex.findall('RoboCop eats baby food. BABY FOOD'))


# import re
# begin_with_hello = re.compile(r"^Hello")
# print(begin_with_hello.search("Hello world"))
# print(begin_with_hello.search("He said 'Hello world'"))
#
# end_with_number = re.compile(r"\d+$")
# print(end_with_number.search("You number is 42"))
# whole_string_is_number = re.compile(r"\d+$")
# print(whole_string_is_number.search("1234567890"))
# print(whole_string_is_number.search("12345xy67890"))


# import re
# at_regex = re.compile(r".at")
# print(at_regex.findall('The cat in the hat sat on the flat mat.'))


# non_greedy_ha_regex = re.compile(r"<.*>")
# print(non_greedy_ha_regex.search("<To server man> for dinner.>").group())
#
# non_greedy_ha_regex = re.compile(r"<.*?>")
# print(non_greedy_ha_regex.search("<To server man> for dinner.>").group())


# import re
# new_line_regex = re.compile(".*", re.DOTALL)
# print(new_line_regex.search('Serve the public truse.\nProtect the innocent.').group())


# import re
# rebocop = re.compile(r'rebocop', re.I)
# print(rebocop.search('Rebocop is part man,part machine,all cop.').group())


# import re
# names_regex = re.compile(r"Agent \w+")
# print(names_regex.sub("CENSORED", 'Agent Alice gave the secret documents to Agent Bob.'))
# agent_names_regex = re.compile(r"Agent (\w)w*")
# print(agent_names_regex.sub(r"\1****", "Agent Alice gave the secret documents to Agent Bob."))


# import re
# re.compile(r"foo", re.VERBOSE)
# re.compile(r"foo", re.T | re.VERBOSE)
#
# text = input("please input text: ")
# ch_len = len(text)
# ch_pw1 = re.compile(r"[a-zA-Z]").search(text)
# ch_pw2 = re.compile(r"\d+").finditer(text)
#
# def ch_pw():
#     if ch_len > 8 and ch_pw1 and ch_pw2:
#         print("correct")
#     else:
#         print("incorrect")
#
# ch_pw()


# import re
# def fn(str_temp, char=r"\s"):
#     str_regex = re.compile(r"^({})*$".format(char, char))
#     s = str_regex.sub("", str_temp)
#     return s
# print(fn(" spam bacon  "))
# print(fn("SpamSpamBaconSpamEggsSpamSpam", "Spam"))


"""
1、有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？
"""
# cnt = 0
# for i in range(5):
#     for j in range(5):
#         for k in range(5):
#             if i != j and i != k and j != k:
#                 result = i*100 + j*10 + k
#                 cnt += 1
#                 print(result)
# print(cnt)
"""
2、企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，
可提成7.5%；20万到40万之间时，高于20万元的部分，可提成5%；40万到60万之间时高于40万元的部分，可提成3%；60万到100万之间时，高于60万元的部分，
可提成1.5%，高于100万元时，超过100万元的部分按1%提成，从键盘输入当月利润I，求应发放奖金总数？

"""
# def method3(I):
#     pro = int(I)
#     profile = {
#         0: 0.1,
#         100000: 0.075,
#         200000:0.05,
#         400000: 0.03,
#         600000: 0.015,
#         1000000: 0.01
#     }
#     profile = dict(sorted(profile.items(), key=lambda x: x[1], reverse=False))
#     ret = 0
#     for i in range(6):
#         if pro > list(profile.keys())[i]:
#             ret += (pro - list(profile.keys())[i]) * list(profile.values())[i]
#             pro = list(profile.keys())[i]
#     print(ret)
#
# II = input("请输入当月利润(元):")
# method3(II)


# from pyspider.libs.base_handler import *


# class Handler(BaseHandler):
#     crawl_config = {
#     }
#
#     @every(minutes=24 * 60)
#     def on_start(self):
#         self.crawl('http://scrapy.org/', callback=self.index_page)
#
#     @config(age=10 * 24 * 60 * 60)
#     def index_page(self, response):
#         for each in response.doc('a[href^="http"]').items():
#             self.crawl(each.attr.href, callback=self.detail_page)
#
#     def detail_page(self, response):
#         return {
#             "url": response.url,
#             "title": response.doc('title').text(),
#         }


# import time
# import functools
#
# class DelayFunc:
#     def __init__(self,  duration, func):
#         self.duration = duration
#         self.func = func
#     def __call__(self, *args, **kwargs):
#         if self.duration > 0:
#             print(f'Wait for {self.duration} seconds...')
#             time.sleep(self.duration)
#             return self.func(*args, **kwargs)
#         else:
#             return self.eager_call(*args, **kwargs)
#     def eager_call(self, *args, **kwargs):
#         print('Call without delay')
#         return self.func(*args, **kwargs)
#
#
# def delay(duration):
#     """
#     装饰器：推迟某个函数的执行。
#     同时提供 .eager_call 方法立即执行
#     """
#     # 此处为了避免定义额外函数，
#     # 直接使用 functools.partial 帮助构造 DelayFunc 实例
#     return functools.partial(DelayFunc, duration)
# @delay(duration=-1)
# def add(a, b):
#     return a + b
# if __name__ == '__main__':
#     print(add)
#     add(3, 5)
#     print(add.func)


# import click
# @click.command()
# @click.option('--count', default=3, help='Number of times to run.')
# @click.option('--name', prompt='Your name', help='The name of the person to greet.')
# def hello(count, name):
#     for x in range(count):
#         click.echo('Hello %s' % name)
#
#
# if __name__ == '__main__':
#     hello()


# from pyzbar.pyzbar import decode
# from PIL import Image
# image = "timg.jpg"
# img = Image.open(image)
# barcodes = decode(img)
# for barcode in barcodes:
#     url = barcode.data.decode("utf-8")
#     print(url)


# from apscheduler.schedulers.blocking import BlockingScheduler
# class ABC:
#     def __init__(self):
#         pass
#
#     def create_page_url(self):
#         pass
#
#     def process(self):
#         scheduler = BlockingScheduler()
#         scheduler.add_job(self.create_page_url, 'cron', hour=2, minute=30, args=())
#         scheduler.start()
#
# if __name__ == '__main__':
#     abc = ABC()
#     abc.process()


# from pymouse import PyMouse
# m = PyMouse()
# m.move(200, 200)
# m.click(200, 200, 1, 2)
# print(m.screen_size())
# print(m.position())


# def is_contain_chinese(check_str):
#     for ch in check_str:
#         if '\u4e00' <= ch <= '\u9fff':
#             return True
#     return False
#
# ret = is_contain_chinese("hello world")
# print(ret)
# ret = is_contain_chinese("我dfadaffd")
# print(ret)


# import datetime
# print(type(datetime.datetime.now()))
# print(datetime.datetime.now())


# import datetime
# dt = datetime.datetime(2015, 10, 21, 16, 29, 0)
# print(type(dt.year))
#
# print(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


# import datetime
# delta = datetime.timedelta(days=11, hours=10, minutes=9, seconds=8)
# print(type(delta))
# print(str(delta))
# print(type(delta.days))
# print(delta.days, delta.seconds, delta.microseconds, delta.total_seconds())
#
# dt = datetime.datetime.now()
# thousand_days = datetime.timedelta(days=1000)
# print(type(dt + thousand_days))
# print(dt + thousand_days)
#
# h = datetime.datetime(2019, 8, 30, 7, 12, 0)
# y = datetime.timedelta(days=365*3)
# print(h)
# print(h - y)
# print(h - (2*y))


# import datetime
# h = datetime.datetime(2019, 8, 30, 7, 12, 0)
# f = h.strftime("%Y/%m/%d %H:%M:%S")
# print(type(f))
# print(f)


# f = "2019/08/30 07:12:00"
# d = datetime.datetime.strptime(f, "%Y/%m/%d %H:%M:%S")
# print(type(d))
# print(d)

#
# print("\u722c\u866b")
#
# print("uni722c".replace("uni", r"\u"))
#
# print("uni722c".replace("uni", r"\u").encode("utf-8").decode("unicode_escape"))


# import asyncio
# async def test():
#     await asyncio.sleep(1)
#     return "test"
# ret = asyncio.run(test())
# print(ret)


# from fontTools.ttLib import TTFont
#
# font = TTFont("demo_file/local_fonts.woff")
# font.saveXML("demo_file/local_fonts.xml")
# print(font.keys())
#
# print(font.getGlyphOrder())
# print(font.getGlyphNames())
#
# print(font.getBestCmap())
# print(font["glyf"]["uniE1A0"].coordinates)
#
# print(font["glyf"]["uniE1A0"].xMin, font["glyf"]["uniE1A0"].yMin, font["glyf"]["uniE1A0"].xMax, font["glyf"]["uniE1A0"].yMax)
#
# print(font["glyf"]["uniE1A0"].flags)
#
# print(font.getGlyphID("uniE1A0"))
#
# font = TTFont("demo_file/local_fonts.woff")


# from fontTools.ttLib import TTFont
# font = TTFont("demo_file/aiding.woff")
# font.saveXML("demo_file/aiding.xml")
# font_names = font.getGlyphOrder()
# print(font_names)
# woff_dict = {}
# for name in font_names[1:]:
#     woff_dict[name.replace("uni", "&#x")] = font.getGlyphID(name) if font.getGlyphID(name) != 10 else 0
#
# print(woff_dict)


# def process():
#     r = requests.get('https://maoyan.com/board/1')
#     woff_path = re.search(r"vfile(.*?)woff", r.text).group()
#     woff_url = f"https://{woff_path}"
#     uni_dict = self.get_uni_num(woff_url)
#     text = r.text
#     for key in uni_dict:
#         text = text.replace(key, uni_dict[key])
#     self.parse_fields(text)


# import asyncio
# from pyppeteer import launch
#
# async def main():
#     browser = await launch({'headless': True})
#     page = await browser.newPage()
#
#     await page.goto("http://example.com")
#     await page.screenshot({"path": "example.png"})
#     await browser.close()
#
# asyncio.get_event_loop().run_until_complete(main())


# from PIL import ImageColor
# print(ImageColor.getcolor("red", "RGBA"))


# from PIL import Image
# img = Image.open("demo_file/debug_error.png")
# width, height = img.size
# name = img.filename
# form = img.format
# img.save("./demo_file/new_cat.jpg")


# from PIL import Image
# im = Image.new("RGBA", (100, 200), "purple")
# im.save("demo_file/purpleImage.png")


# from PIL import Image
# from PIL import ImageColor
# img = Image.open("demo_file/purpleImage.png")
# x, y = 12, 66
# r, g, b, alpha = img.getpixel((x, y))
# img.putpixel((x, y), (210, 210, 210))
# img.putpixel((x, y), ImageColor.getcolor("green", "RGBA"))
# img.save("demo_file/putpixel.png")


# from PIL import Image
# im = Image.open("demo_file/purpleImage.png")
# crop = im.crop((25, 30, 45, 50))
# crop.save("demo_file/new.png")


# from PIL import Image
# im = Image.open("demo_file/purpleImage.png")
# imcopy = im.copy()
# imcopy.save("demo_file/imcopy.png")


from PIL import Image
# im = Image.open("demo_file/purpleImage.png")
# crop = Image.new("RGBA", (23, 23), "green")
# w, h = im.size
# c_w, c_h = crop.size
# im2 = im.copy()
# for left in range(0, w, c_w):
#     for top in range(0, h, c_h):
#         im2.paste(crop, (left, top))
# im2.save("demo_file/paste.png")


# from PIL import Image
# im  = Image.open("demo_file/purpleImage.png")
# resize_img = im.resize((5, 8))
# resize_img.save("demo_file/resize_img.png")


# from PIL import Image
# im = Image.open("demo_file/purpleImage.png")
# im.rotate(30, expand=True).save("demo_file/rotate.png")
# im.transpose(Image.FLIP_LEFT_RIGHT).save("demo_file/right.png")
# im.transpose(Image.FLIP_TOP_BOTTOM).save("demo_file/top.png")


# xml_text = '<?xml version="1.0" encoding="ISO-8859-1"?><note><to>George</to><from>John</from><heading>Reminder</heading><body>Do not forget the meeting!</body></note>'
# url = "http://web.chacuo.net/formatxml"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
#     "Host": "web.chacuo.net",
#     "X-Requested-With": "XMLHttpRequest",
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
# }
# form_data = {"data": xml_text, "type": "format", "beforeSend": "undefined"}
# resp = requests.post(url, data=form_data, headers=headers)
# print(resp.json()["data"][0])


# import requests
# import xmltodict
#
#
# def pretty_xml(text: str) -> str:
#     url = "http://web.chacuo.net/formatxml"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
#         "Host": "web.chacuo.net",
#         "X-Requested-With": "XMLHttpRequest",
#         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#     }
#     form_data = {"data": text, "type": "format", "beforeSend": "undefined"}
#     resp = requests.post(url, data=form_data, headers=headers)
#     print(resp.json()["data"][0])
#     return resp.json()["data"][0]
#
# def save_mxl(pretty_xml_str: str):
#     with open("demo_file/test.mxl", "w", encoding="utf-8") as f:
#         f.write(pretty_xml_str)
#
# def xml_to_dict(format_ed_xml: str) -> dict:
#     dict_xml = xmltodict.parse(format_ed_xml)
#     print(f"\n>>>>{dict_xml['note']['body']}")
#
#
# if __name__ == '__main__':
#     xml_text = '<?xml version="1.0" encoding="ISO-8859-1"?><note><to>George</to><from>John</from><heading>Reminder</heading><body>Do not forget the meeting!</body></note>'
#     format_xml = pretty_xml(xml_text)
#     xml_to_dict(format_xml)
#     save_mxl(format_xml)


# import requests
# r = requests.get("https://www.baidu.com")
# print(r.status_code)
# print(type(r))
# print(r.headers)
# print(r.encoding)
# print(r.apparent_encoding)
# r.encoding = "utf-8"
# print(r.encoding)


1
def get_html_text(url):
    try:
        r = requests.get(url, timeout=5)
        print(r.raise_for_status())
        # r.encoding = r.apparent_encoding
        # return r.text
        return r.content.decode('utf8')
    except:
        return "Error"

if __name__ == '__main__':
    url = "http://www.baidu.com"
    res = get_html_text(url)
    print(res)