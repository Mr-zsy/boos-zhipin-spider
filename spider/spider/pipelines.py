# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 用于清理html数据，验证检查处理爬取数据，将爬取数据保存到数据库
# 将setting导入，以使用定义内容
from scrapy.conf import settings
import pymongo
import re
import time

class SpiderPipeline(object):
    def __init__(self):
        #连接数据库
        host = settings['MONGO_URI']
        port = settings['MONGO_PORT']
        dbName = settings['MONGO_DB']
        self.client = pymongo.MongoClient(host=host, port=port)
        # 定义数据库
        db = self.client[dbName]
        self.table = db[settings['MONGO_COLLECTION']]
    def process_item(self, item, spider):
        if '-' in item['maxPayment']:
            item['maxPayment'] = item['maxPayment'][1:]
        if 'k' in item['maxPayment']:
            item['maxPayment'] = item['maxPayment'][0:-1]
        if 'k' in item['minPayment']:
            item['minPayment'] = item['minPayment'][0:-1]
        item['minPayment'] = int(item['minPayment'])
        item['maxPayment'] = int(item['maxPayment'])



        # print(item)
        if re.match('(0|1)[0-9]月[0-9]{2}日',item['updateTime']) == None:

            #今天
            if re.match('[0-9]{2}:[0-9]{2}',item['updateTime']) != None:
                print('今天')
                today = time.localtime(time.time())
                month = today[1]
                day = today[2]
                if month < 10:
                    month = '0' + str(month)
                if day < 10:
                    day = '0' + str(day)
                item['updateTime'] = str(month)+'月'+str(day)+'日'
                item['updateMonth'] = month
            #昨天
            if item['updateTime'] == '昨天':
                print('昨天')
                yesterday = time.localtime(time.time() - 24*60*60)
                month = yesterday[1]
                day = yesterday[2]
                if month < 10:
                    month = '0' + str(month)
                if day < 10:
                    day = '0' + str(day)
                item['updateTime'] = str(month) + '月' + str(day) + '日'
                item['updateMonth'] = month


        item['updateMonth'] = int(item['updateMonth'])

        #存库----------------
        # if not self.table.find_one(dict(item)):
        #     # print(item)
        #     self.table.insert_one(dict(item))
        #关闭数据库连接
        self.client.close()
        return item
