import random
import time

import requests

ip = '16.79.112.218'
port = 9254

proxys = {
    # "http": f"http://{ip}:{port}",
    # "https": f"http://{ip}:{port}",
}


headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cache-Control": "no-cache",
    # "Connection": "keep-alive",
    # "Pragma": "no-cache",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",

}


def gen_uuid():
    # 生成随机数（对应 JavaScript 的 Math.random() * Number.MAX_SAFE_INTEGER）
    random_part = random.randint(0, 2 ** 53 - 1)  # Number.MAX_SAFE_INTEGER = 2^53 - 1
    # 转换为十六进制字符串
    random_hex = hex(random_part)[2:]  # [2:] 去掉 '0x' 前缀

    # 获取当前时间戳（毫秒），对应 JavaScript 的 new Date().getTime()
    timestamp = int(time.time() * 1000)
    timestamp_hex = hex(timestamp)[2:]

    # 拼接结果
    return f"{random_hex}-{timestamp_hex}"

# cookies = {
#     # "__mta": "48585497.1770175514299.1770176000052.1770176057568.4",
#     # "_lxsdk_cuid": "19c26aebe36c8-04e4ff1e1555e48-26061d51-1bcab9-19c26aebe36c8",
#     # "_ga": "GA1.1.1142392262.1770175513",
#     # "uuid_n_v": "v1",
#     "uuid": "5D008CF01DFB11F1B6F32901BFF84A677103CBC0AAD440F28168D09B0F1278B4",
#     # "_lxsdk": "5D008CF01DFB11F1B6F32901BFF84A677103CBC0AAD440F28168D09B0F1278B4",
#     # "_csrf": "212c6a45586c1910e39297fae4a14d173943c171e9f4e37adef922884a59a945",
#     # "Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533": "1773310093,1773994766",
#     # "Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533": "1773994766",
#     # "HMACCOUNT": "22F94829BF4DAF2D",
#     # "_ga_WN80P4PSY7": "GS2.1.s1773994766$o4$g0$t1773994766$j60$l0$h0",
#     # "_lxsdk_s": "19d0a53eef5-19d-c0a-3ea%7C%7C2"
# }
url = "https://www.maoyan.com/board/4"
response = requests.get(url, headers=headers, cookies={
    'uuid': gen_uuid()
}, proxies=proxys)

print(response.text)
print(response)
with open("maoyan_verify.html", "wb") as f:
    f.write(response.content)