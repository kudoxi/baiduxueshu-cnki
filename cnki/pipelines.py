# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .settings import *
import pymysql

class CnkiPipeline(object):
    def process_item(self, item, spider):
        return item

#存到mysql的管道类
class CnkiMysqlPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(MYSQL_HOST,MYSQL_USER,MYSQL_PSWD,MYSQL_DB,charset=MYSQL_CHAR)
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        ins = "insert into article (title,content) values('%s','%s')"%(item['title'],item['content'])
        print(ins)
        self.cursor.execute(ins)
        self.db.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()