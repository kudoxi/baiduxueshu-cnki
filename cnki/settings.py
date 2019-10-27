# -*- coding: utf-8 -*-

# Scrapy settings for cnki project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cnki'

SPIDER_MODULES = ['cnki.spiders']
NEWSPIDER_MODULE = 'cnki.spiders'
LOG_LEVEL = 'INFO'
FEED_EXPORT_ENCODING = 'utf-8'
SELENIUM_TIMEOUT = 25           # selenium浏览器的超时时间，单位秒
LOAD_IMAGE = False               # 是否下载图片
WINDOW_HEIGHT = 900             # 浏览器窗口大小
WINDOW_WIDTH = 900


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cnki (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 20

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'deflate',
    # 'Referer': 'https://kns.cnki.net/kns/brief/default_result.aspx',
    # 'Cookie': 'Ecp_ClientId=3190702230503361357; cnkiUserKey=99c784be-af04-a2f0-bb9f-d2d1f41da8eb; RsPerPage=20; ASP.NET_SessionId=ot2osn2cwila5adg1zp5sbmi; Ecp_IpLoginFail=19102660.177.243.98; SID_kns=123123; SID_klogin=125144; KNS_SortType=; SID_crrs=125131; _pk_ref=%5B%22%22%2C%22%22%2C1572092055%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*; SID_krsnew=125132',
    # 'Cookie': 'BAIDUID=8C1CB2F065B39F5C08E86B8F65642206:FG=1; BIDUPSID=8C1CB2F065B39F5C08E86B8F65642206; PSTM=1554817591; MCITY=-%3A; H_WISE_SIDS=131127_126125_131449_131869_131365_128066_120141_132313_132440_130763_132393_132378_132326_132213_131518_132260_118887_118867_131401_118845_118833_118805_132211_131651_131577_131535_131533_131529_130222_131294_131872_131391_129564_131796_132590_131396_130125_132239_131874_130569_131196_129653_127027_131861_132558_131688_132542_131036_131906_132294_129838_129373_132308_129644_132204_130828_131424_132416_131443_110085_127969_131506_123289_131749_127316_130604_127417_131828_128602_131258_131925; BDUSS=p2ZHhRYlgwWjdmbkRQcjhYTXJDdUctT05-YmdQQ01NaHYyZVhYVmwtWlpQTFJkSVFBQUFBJCQAAAAAAAAAAAEAAAA1q5VEue25yL6yy74AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFmvjF1Zr4xdY1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_f28578486a5410f35e6fbd0da5361e5f=1572098288; BD_CK_SAM=1; BDSVRTM=572; H_PS_PSSID=1434_21125_29567_29221; delPer=0; PSINO=5'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'cnki.middlewares.CnkiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'cnki.middlewares.SeleniumMiddleware':400,
    'cnki.middlewares.CnkiDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'cnki.pipelines.CnkiPipeline': 300,
    'cnki.pipelines.CnkiMysqlPipeline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# mysql config
#create database cnki DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
#create table article (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, title varchar(255) null,content longtext not null)charset=utf8;
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PSWD = 'root'
MYSQL_DB = 'cnki'
MYSQL_CHAR = 'utf8'