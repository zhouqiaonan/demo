# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class Maoyan100SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class Maoyan100DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class EncryptedCookieMiddleware:
    def process_request(self, request, spider):
        uuid_val = self.gen_uuid()
        request.cookies = {
            "__mta": "48585497.1770175514299.1773310119143.1774850679516.5",
            "_lxsdk_cuid": "19c26aebe36c8-04e4ff1e1555e48-26061d51-1bcab9-19c26aebe36c8",
            "_ga": "GA1.1.1142392262.1770175513",
            "uuid_n_v": "v1",
            "uuid": uuid_val,
            "_lxsdk": "5D008CF01DFB11F1B6F32901BFF84A677103CBC0AAD440F28168D09B0F1278B4",
            "_csrf": "192ffe50551517236e8e42a13538e71238a2234c2cf28fd161f172a0d8f62d72",
            "_lx_utm": "utm_source%3Dgoogle%26utm_medium%3Dorganic",
            "Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533": "1774237099,1774408633,1774600328,1774850672",
            "HMACCOUNT": "22F94829BF4DAF2D",
            "hotMovieIds": "1324725,1565122,1530979,1531786,343635,1522280,1550491,1501297,1340084,1563473,1608703,1489992,1459929,1609913,1322781,1592115,1218142,1625533,1565327,1581746,1593791,1552123,338436,78463,1443455,43999,1310584,1548780,1563675,1565319,1612199,490367,1443396,1528992,1606500,1572470,1636263,1536541,1528920,1501854,1323,1522597,1532745,1522567,1204596,1530742,1577698,1198213,1435004,1301939,1407233,1526307,1384725,1516934,1580307,1581178,1573927,1582773,1631435,1603175,1455619",
            "old-moviepage-ci": "50",
            "_ga_WN80P4PSY7": "GS2.1.s1774850672$o10$g1$t1774850700$j32$l0$h0",
            "Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533": "1774850701",
            "_lxsdk_s": "19d3d57f590-f64-363-c97%7C%7C8"
        }
        return None

    def gen_uuid(self):
        random_part = random.randint(0, 2 ** 53 - 1)  # Number.MAX_SAFE_INTEGER = 2^53 - 1
        # 转换为十六进制字符串
        random_hex = hex(random_part)[2:]  # [2:] 去掉 '0x' 前缀

        # 获取当前时间戳（毫秒），对应 JavaScript 的 new Date().getTime()
        timestamp = int(time.time() * 1000)
        timestamp_hex = hex(timestamp)[2:]

        # 拼接结果
        return f"{random_hex}-{timestamp_hex}"
