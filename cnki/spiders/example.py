# -*- coding: utf-8 -*-
import scrapy
from cnki.items import CnkiItem
from selenium import webdriver
import urllib.parse
import re
import math
from http.cookiejar import CookieJar
# win10 print 输出问题
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class ExampleSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['xueshu.baidu.com']
    start_urls = ['http://xueshu.baidu.com']

    def __init__(self):
        super(ExampleSpider, self).__init__()
        options = webdriver.ChromeOptions()
        options.set_headless()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

        self.home_url = 'http://xueshu.baidu.com/s?'
        self.key_word = '灌料对照'
        self.cant_contain = ['马铃薯','甘薯','木薯','豆薯']
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        print("一级入口页面")
        data = {
            'wd': self.key_word,
            'tn': 'SE_baiduxueshu_c1gjeupa',
            'cl': 3,
            'ie': 'utf-8',
            'sc_f_para': 'sc_tasktype={firstAdvancedSearch}',
            'filter': 'sc_year={2015,+}',
        }
        query_string = urllib.parse.urlencode(data)
        url = self.home_url + query_string
        print('url:', url)
        yield scrapy.Request(url=url,
                      callback=self.parse_page)

    # 解析分页
    def parse_page(self, response):
        print('列表页面')
        # totalline = response.xpath("//div[@id='toolbar']/span[@class='nums']").extract()[0]
        # total_arr = re.findall(r'[1-9]+\.?[0-9]*', totalline)
        # total_num = ''.join(total_arr)
        # pagenum = math.ceil(int(total_num) / 10)
        # 网页上显示的是假的，真实没有80100多个结果
        pagenum = 71 # 拟定
        print('pagenum:', pagenum)
        for i in range(1, pagenum + 1):
            pn = (i - 1) * 10
            print('pn:', pn)
            data = {
                'wd': self.key_word,
                'tn': 'SE_baiduxueshu_c1gjeupa',
                'cl': 3,
                'ie': 'utf-8',
                'sc_f_para': 'sc_tasktype={firstAdvancedSearch}',
                'filter': 'sc_year={2015,+}',
                'pn': pn,
                'sc_hit': 1
            }
            query_string = urllib.parse.urlencode(data)
            url = self.home_url + query_string
            print('url:', url)
            yield scrapy.Request(url=url,
                                 headers={"Referer": url},
                                cookies={CookieJar: 1},
                                 callback=self.parse_two_link)

    # 二级页面-解析列表
    def parse_two_link(self, response):
        print("进入二级")
        # con = response.body.decode('utf-8')
        # print(con)
        contentlist = response.xpath("//div[@class='sc_content']")
        for content in contentlist:
            title = content.xpath("..//h3//a").extract()[0]
            titles = re.findall('<a.*?target="_blank">(.*?)</a>', title, re.S)
            if len(titles):
                title = titles[0].replace('<em>', '')
                title = title.replace('</em>', '')
                cant_use = 0
                for cant in self.cant_contain:
                    if cant in title:
                        cant_use = 1
                if cant_use != 1:
                    item = CnkiItem()
                    item['title'] = title
                    yield item
