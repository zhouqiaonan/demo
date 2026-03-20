# import requests
#
# try:
#     user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}
#     r = requests.get('https://www.baidu.com', timeout=5, headers=user_agent)
#     r.raise_for_status()
#     print(r.text)
#     print(r.status_code)
#     print(r.encoding)
#     print(r.apparent_encoding)
#     print(r.request.headers)
# except Exception as e:
#     print(e)


# import requests
#
# r = requests.get('https://www.python123.io/ws/demo.html')
# # print(r.text)
# demo = r.text
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(demo, 'html.parser')
# print(soup.prettify())
# tag = soup.p.string
# print(tag)


# from bs4 import BeautifulSoup
# new_soup = BeautifulSoup("<b><!--this is a test--><p>this is a comment</p>", "html.parser")
# print(new_soup.b.string)
# print(new_soup.p.string)




