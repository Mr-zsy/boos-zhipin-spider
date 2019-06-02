from bs_spider.settings import settings
import pymongo
import re
import time

class DataClean(object):
    def __init__(self):
        #连接数据库
        host = settings['MONGO_URI']
        port = settings['MONGO_PORT']
        dbName = settings['MONGO_DB']
        self.client = pymongo.MongoClient(host=host, port=port)
        # 定义数据库
        db = self.client[dbName]
        self.table = db[settings['MONGO_COLLECTION']]

    def dataClean(self, item):
        if '-' in item['maxPayment']:
            item['maxPayment'] = item['maxPayment'][1:]
        if 'k' in item['maxPayment']:
            item['maxPayment'] = item['maxPayment'][0:-1]
        if 'k' in item['minPayment']:
            item['minPayment'] = item['minPayment'][0:-1]
        item['minPayment'] = int(item['minPayment'])
        item['maxPayment'] = int(item['maxPayment'])

        # print(item)
        if re.match('(0|1)[0-9]月[0-9]{2}日', item['updateTime']) == None:

            # 今天
            if re.match('[0-9]{2}:[0-9]{2}', item['updateTime']) != None:
                print('今天')
                today = time.localtime(time.time())
                month = today[1]
                day = today[2]
                if month < 10:
                    month = '0' + str(month)
                if day < 10:
                    day = '0' + str(day)
                item['updateTime'] = str(month) + '月' + str(day) + '日'
                item['updateMonth'] = month
            # 昨天
            if item['updateTime'] == '昨天':
                print('昨天')
                yesterday = time.localtime(time.time() - 24 * 60 * 60)
                month = yesterday[1]
                day = yesterday[2]
                if month < 10:
                    month = '0' + str(month)
                if day < 10:
                    day = '0' + str(day)
                item['updateTime'] = str(month) + '月' + str(day) + '日'
                item['updateMonth'] = month

        item['updateMonth'] = int(item['updateMonth'])

        # 存库----------------
        if not self.table.find_one(dict(item)):
            # print(item)
            self.table.insert_one(dict(item))