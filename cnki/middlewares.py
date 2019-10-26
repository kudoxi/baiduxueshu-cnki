# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from logging import getLogger
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# class SeleniumMiddleware():
#     #经常需要在pipeline或者中间件中获取settings的属性，可以通过scrapy.crawler.Crawler.settings属性
#
#     dcap = DesiredCapabilities.PHANTOMJS.copy()
#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.settings
#         # 从settings.py中，提取selenium设置参数，初始化类
#         return cls()
#
#     def __init__(self):
#         self.logger = getLogger(__name__)
#         options = webdriver.ChromeOptions()
#         options.set_headless()
#         options.add_argument('lang=zh_CN.UTF-8')
#         options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
#
#         self.browser = webdriver.Chrome(options=options)
#
#     def process_request(self, request, spider):
#         '''
#         用chrome抓取页面
#         :param request: Request请求对象
#         :param spider: Spider对象
#         :return: HtmlResponse响应
#         '''
#         # self.logger.debug('chrome is getting page')
#         # 依靠meta中的标记，来决定是否需要使用selenium来爬取
#         usedSelenium = request.meta.get('usedSelenium', False)
#         if usedSelenium:
#             print("chrome is getting page")
#             self.browser.get(request.url)
#             try:
#                 return HtmlResponse(url=request.url,body=self.browser.page_source,status=200, request=request,encoding='utf-8')
#             except Exception as e:
#                 # self.logger.debug(f'chrome getting page error, Exception = {e}')
#                 print("chrome getting page error, Exception :",e)
#                 return HtmlResponse(url=request.url, status=500, request=request)
#
#         else:
#             print("use no selenium")
#             #time.sleep(3)
#             # return None
#             return HtmlResponse(url=request.url, body=self.browser.page_source,request=request,encoding='utf-8',status=200)
#


class CnkiSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CnkiDownloaderMiddleware(object):
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
        spider.logger.info('Spider opened: %s' % spider.name)
