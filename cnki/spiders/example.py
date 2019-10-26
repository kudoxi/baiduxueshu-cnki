# -*- coding: utf-8 -*-
import scrapy
from cnki.items import CnkiItem
from selenium import webdriver
import urllib.parse
import re
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
        self.key_word = '氮肥'
        self.max_page = 50
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        print("一级页面")
        data = {
            'wd': self.key_word,
            'tn': 'SE_baiduxueshu_c1gjeupa',
            'cl': 3,
            'ie': 'utf-8',
            'sc_f_para': 'sc_tasktype={firstAdvancedSearch}',
            'filter': 'sc_year={2015,+}'
        }
        query_string = urllib.parse.urlencode(data)
        url = self.home_url + query_string
        print('url:', url)
        yield scrapy.Request(url=url,
                      meta={'usedSelenium': True, 'dont_redirect': True},
                      callback=self.parse_two_link)

    # 二级页面-解析列表
    def parse_two_link(self, response):
        print("进入二级")
        # con = response.body.decode('utf-8')
        # print(con)
        contentlist = response.xpath("//div[@class='sc_content']")
        for content in contentlist:
            title = content.xpath("..//h3//a").extract()[0]
            print('1111', title)
            titles = re.findall('<a.*?target="_blank">(.*?)</a>', title, re.S)
            if len(titles):
                title = re.sub('[<em>]', '', titles[0])
                title = re.sub('[</em>]', '', titles[0])
                print(title)
                item = CnkiItem()
                item['title'] = title
                item['content'] = '1'
                yield item
