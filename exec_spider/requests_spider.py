# import requests
# url = "http://baidu.com"
# response = requests.get(url)
# print(response)

# import requests
#
# data = {
#     "name": "编程帮",
#     "url": "www.biancheng.com",
# }
#
# response = requests.get("http://httpbin.org/get", params=data)
# print(response.text)


# import requests
# url = "https://fanyi.baidu.com"
# data = {
#     "from": "zh",
#     "to": "en",
#     "query": "编程帮www.biancheng.com你好"
# }
#
# response = requests.post(url, data=data)
# # print(response.text)
# print(response.encoding)
# print(response.status_code)
# print(response.url)
# print(response.headers)
# print(response.cookies)

# import requests
#
#
# headers = {
#     "Host": "img0.baidu.com",
#     "pragma": "no-cache",
#     "cache-control": "no-cache",
#     "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "sec-fetch-site": "none",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-user": "?1",
#     "sec-fetch-dest": "document",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "priority": "u=0, i"
# }
# cookies = {
#     "BIDUPSID": "3B18893470ADE76B3C10A9610916CACD",
#     "PSTM": "1764205819",
#     "BAIDUID": "DF7541311B0CCF1B6A8A1184BD6A067F:FG=1",
#     "H_WISE_SIDS_BFESS": "60271_63148_66580_66694_66686_67050_67051_67109_66951_67152_67157_67181_67222_67238_67266_67295_67318_67317_67314_67323_67320_67415_67451_67473_67463_67496_67505_67563_67568_67550_67543",
#     "BAIDUID_BFESS": "DF7541311B0CCF1B6A8A1184BD6A067F:FG=1",
#     "__bid_n": "19ac2dd97c18592f892373",
#     "MCITY": "-%3A",
#     "ZFY": "5Ekvp7v:AfRrX9:A:AYcCq4KV9xj2Zky02UKfX677dBLq4:C",
#     "BDRCVFR[dG2JNJb_ajR]": "mk3SLVN4HKm",
#     "H_PS_PSSID": "60271_63148_67861_67885_67886_67964_68042_67984_68132_68146_68144_68151_68150_68139_68165_68191_68224_68232_68254_68261_68263_68283_68292_68302_68379_68358_68422_68412_68436_68455_68446",
#     "delPer": "0",
#     "PSINO": "5",
#     "BA_HECTOR": "04258k04800k2g8la400842ha5042l1ks4evq27",
#     "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
#     "H_WISE_SIDS": "67886_67964_68042_67984_68146_68144_68151_68150_68139_68165_68224_68254_68263_68292_68379_68358_68422_68412_68455_68446",
#     "ab_sr": "1.0.1_MGIzNTcyNWUzMTMxNjcxYTAyYjYzODUwNDk2MTkyYTk0ZGZjYjA1ZWU2MDJhNTRlMDg5MTBlYTM0YWFkODIyOTMwMzBjN2I1MDFhNjhlMmM3NjdlNDdjMDNmMDVkYTI3YTQ3MDgxZjNiMzJlMzIzM2Y0NDI4ZDJmYzcxNmE5ZTMzZGJmZDFjNzkzYmU3MDllMTg5MzI0NjEwZmQyYTY3OA==",
#     "RT": "\"z=1&dm=baidu.com&si=2a3144a1-75d1-4ed4-9d13-6a0a1c86631b&ss=mn480faw&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=260&ul=2scgf&hd=2scgw\""
# }
# url = "https://img0.baidu.com/it/u=1213867596,3883731737&fm=253&fmt=auto&app=138&f=JPEG"
# response = requests.get(url, headers=headers, cookies=cookies)
#
# print(response.text)
# print(response)

# -*- coding:utf8 -*-
import requests
import re
from urllib import parse
import os


class BaiduImageSpider(object):
    def __init__(self):
        self.url = "https://image.baidu.com/search/flip?tn=baiduimage&word={}"
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}

    def get_images(self, url, word):
        res = requests.get(url, headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        # print(html)
        pattern = re.compile('"hoverURL":"(.*?)"', re.S)
        img_link_lst = pattern.findall(html)
        print(img_link_lst)

        dirtory = "./data/"
        cnt = 0
        for img_link in img_link_lst:
            cnt += 1
            filename = f"{dirtory}{word}_{cnt}.jpg"
            self.save_image(img_link, filename)

    def save_image(self, img_link, filename):
        html = requests.get(img_link, headers=self.headers).content
        with open(filename, "wb") as f:
            f.write(html)
        print(f"{filename} 下载成功!")

    def run(self):
        word = input("您想要谁的照片?")
        word_parse = parse.quote(word)
        url = self.url.format(word_parse)
        self.get_images(url, word)

if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.run()
