from scrapy import cmdline
import os

def startSpider():
    #启动mongodb
    os.system('mongod --dbpath /usr/local/mongodb/data/db --bind_ip 127.0.0.1')
    # print('fuck')

    # 开启爬虫
    cmdline.execute('scrapy crawl recruitment'.split())


# startSpider()