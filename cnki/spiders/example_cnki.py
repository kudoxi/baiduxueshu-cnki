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
    start_urls = ['https://kns.cnki.net/kns/brief/result.aspx?dbprefix=scdb']

    def __init__(self):
        super(Example2Spider, self).__init__()
        self.home_url = 'https://kns.cnki.net/kns/request/SearchHandler.ashx?'
        self.cur_referer = 'https://kns.cnki.net/kns/brief/result.aspx?dbprefix=scdb'
        self.list_url = 'https://kns.cnki.net/kns/brief/brief.aspx?'
        self.key_word = '氮肥' #'灌水对照'
        self.cookie = {
                          'Ecp_ClientId': '3190702230503361357',
                          'cnkiUserKey': '99c784be-af04-a2f0-bb9f-d2d1f41da8eb',
                          'RsPerPage': '50',
                          'ASP.NET_SessionId': 'lo5hjrrm21kdzlg5cxdwdfgm',
                          'Ecp_IpLoginFail': '191027115.197.222.231',
                          'SID_kns': '123106',
                          'SID_klogin': '125144',
                          'KNS_SortType': '',
                          '_pk_ref': '%5B%22%22%2C%22%22%2C1572156598%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D',
                          ' _pk_ses': '*',
                          'SID_krsnew': '125133',
                          'SID_crrs': '125132'
                      }

    # 入口检索页
    def parse(self, response):
        data = {
            'NaviCode': '*',
            'ua': '1.21',
            "PageName": "ASP.brief_default_result_aspx",
            'isinEn': 1,
            "DbPrefix": "SCDB",
            'DbCatalog': '中国学术期刊网络出版总库',
            "ConfigFile": "SCDB.xml",
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            'publishdate_from': '2015-01-01',
            "txt_1_sel": 'SU$%=|',
            'txt_1_value1': self.key_word,
            'txt_1_relation': '#CNKI_AND',
            'his': '0',
            '__': time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)',
        }
        query_string = urllib.parse.urlencode(data)
        yield scrapy.Request(url=self.home_url + query_string,
                      headers={"Referer": self.cur_referer,
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
                               "Host": "kns.cnki.net",
                               },
                      cookies=self.cookie,
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
        query_string = urllib.parse.urlencode(data)
        query_string = query_string.lower()
        url = self.list_url + '?' + query_string
        # url = 'https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&isinEn=1&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1572097267437&keyValue=%E7%81%8C%E6%B0%B4%E5%AF%B9%E7%85%A7&S=1&sorttype='
        print("二级链接：", url)
        yield scrapy.Request(url=url,
                      headers={"Referer": self.cur_referer,
                               "Connection": "keep-alive",
                               "Sec-Fetch-Mode": "nested-navigate",
                               "Sec-Fetch-Site": "same-origin",
                               "Sec-Fetch-User": "?1",
                               "Upgrade-Insecure-Requests": "1"
                               },
                      cookies=self.cookie,
                      callback=self.parse_list_first)

    # 解析列表
    def parse_list_first(self, response):
        print('解析页面')

        con = response.body.decode('utf-8')
        print(con)
        # page_link = response.xpath('//span[@class="countPageMark"]/text()').extract_first()
        # print("page_link:", page_link)
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
        # item = CnkiItem()
        # item['title'] = page_link
        # item['content'] = page_link
        # yield item
        # print('over')