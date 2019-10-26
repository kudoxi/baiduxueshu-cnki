# -*- coding: utf-8 -*-
import scrapy
from cnki.items import CnkiItem
from selenium import webdriver
import time
import urllib.parse
from http.cookiejar import CookieJar

class Example2Spider(scrapy.Spider):
    name = 'cnki2'
    allowed_domains = ['kns.cnki.net']
    start_urls = ['https://kns.cnki.net/kns/brief/brief.aspx']

    def __init__(self):
        super(Example2Spider, self).__init__()
        options = webdriver.ChromeOptions()
        options.set_headless()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

        self.home_url = 'https://kns.cnki.net/kns/brief/default_result.aspx?'
        self.cur_referer = 'https://kns.cnki.net/kns/brief/default_result.aspx'
        self.list_url = 'https://kns.cnki.net/kns/brief/brief.aspx'
        self.key_word = '氮肥' #'灌水对照'
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        data = {
            "txt_1_sel": "SU$%=|",
            "txt_1_value1": self.key_word,
            "txt_1_special1": "%",
            "PageName": "ASP.brief_default_result_aspx",
            "ConfigFile": "SCDBINDEX.xml",
            "dbPrefix": "CJFQ",
            "db_opt": "CJFQ",
            "singleDB": "CJFQ",
            "db_codes": "CJFQ",
            "his": 0,
            "formDefaultResult": "",
            "ua": "1.11",
            "__": time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)'
        }
        query_string = urllib.parse.urlencode(data)
        yield scrapy.Request(url=self.home_url + query_string,
                      headers={"Referer": self.cur_referer},
                      cookies={CookieJar: 1},
                      callback=self.parse_two_link)

    # 二级页面-iframe 列表
    def parse_two_link(self, response):
        print("进入二级")
        data = {
            'pagename': 'ASP.brief_default_result_aspx',
            'dbPrefix': 'SCDB',
            'dbCatalog': '中国学术期刊网络出版总库',
            'ConfigFile': 'SCDBINDEX.xml',
            'research': 'off',
            't': int(time.time()),
            'keyValue': self.key_word,
            'S': '1',
            "recordsperpage": 50,
            'isinEn': 1,
            'sorttype': ""
        }
        # query_string = urllib.parse.urlencode(data)
        # query_string = query_string.lower()
        # url = self.list_url + '?' + query_string
        url = 'https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&isinEn=1&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1572097267437&keyValue=%E7%81%8C%E6%B0%B4%E5%AF%B9%E7%85%A7&S=1&sorttype='
        print("二级链接：", url)
        yield scrapy.Request(url=url,
                      headers={"Referer": self.cur_referer},
                      callback=self.parse_list_first)

    # 解析列表
    def parse_list_first(self, response):
        print('解析页面')
        print(response.text)
        page_link = response.xpath('//span[@class="countPageMark"]/text()').extract_first()
        print("page_link:", page_link)
        # max_page = int(page_link.split("/")[1])
        # print("max_page:", max_page)
        # data = {
        #     "curpage": page_num,  # 循环更改
        #     "RecordsPerPage": 50,
        #     "QueryID": 0,
        #     "ID": "",
        #     "turnpage": 1,
        #     "tpagemode": "L",
        #     "dbPrefix": "CJFQ",
        #     "Fields": "",
        #     "DisplayMode": "listmode",
        #     "PageName": "ASP.brief_default_result_aspx",
        #     "isinEn": 1
        # }
        item = CnkiItem()
        item['title'] = page_link
        item['content'] = page_link
        yield item
        print('over')