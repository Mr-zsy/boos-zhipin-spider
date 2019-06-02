# -*- coding: utf-8 -*-
import scrapy
from spider.spider.items import SpiderItem
from spider.spider.cookie_util import getCookie
from spider.spider.user_agent_util import getUserAgent
from selenium import webdriver
from scrapy.utils.project import get_project_settings
import requests
import time
import json
import random



class MainSpider(scrapy.Spider):
    #项目的唯一名字，用来区分不同的爬虫
    name = 'recruitment'
    #允许爬取的域名
    allowed_domains = ['www.zhipin.com']
    #spider启动时爬取的url
    start_urls = ['https://www.zhipin.com']
    #对settings中的值进行覆盖
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'spider.spider.middlewares.RandomHeaderMiddleware': 541,
            'spider.spider.middlewares.ProxyMiddleWare': 542,
            'spider.spider.middlewares.TestMiddleWare': 543
        }
    }

    def __init__(self):
        super(MainSpider, self).__init__()
        #设置参数
        # self.mySetting = get_project_settings()
        # self.timeout = self.mySetting.get('SELENIUM_TIMEOUT')
        self.myProxy = self.getProxy()
        self.myCookie = getCookie()
        # self.myHeader = get
        self.meta = self.getProxy()
        self.myUserAgent = getUserAgent()


        # self.kindList = ['Python', "Java", "Web前端", 'C++']
        self.kindList = [ "Web前端", 'C++']
        # self.baseList = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '成都', '武汉']
        self.baseList = [
            {"北京":"101010100"},
            {"上海":"101020100"},
            {"广州":"101280100"},
            {"深圳":"101280600"},
            {"杭州":"101210100"},
            {"天津":"101030100"}
        ]
        self.kindListIndex = 0
        self.baseListIndex = 0
        # self.spiderContent = {
        #     'kind':'Python',
        #     'base':'北京'
        # }
        self.spiderContent = {
            'kind': 'Web前端',
            'base': '101010100'
        }


    #获取代理ｉｐ
    @classmethod
    def getProxy(cls):
        proxy = requests.get('http://127.0.0.1:3289/pop')
        proxy_json = json.loads(proxy.text)
        # return {"proxy": proxy_json.get('http', proxy_json.get('https'))}
        return proxy_json.get('http', proxy_json.get('https'))


    def start_requests(self):
        print('启动~')
        requestUrl = 'https://www.zhipin.com/job_detail/?query={}&city={}&industry=&position='.format(self.spiderContent['kind'], self.spiderContent['base'])
        yield scrapy.Request(url=requestUrl, cookies=self.myCookie['dictCookie'])  # 这里带着cookie发出请求


        #请求start_urls后返回的响应作为唯一参数传给此函数
    def parse(self, response):
        requestUrl = ''
        # job_list = response.css('#main > div > div.job-list > ul')
        # if not job_list:
        #     print('被封了~')
        #     requestUrl = 'https://www.zhipin.com/job_detail/?query={}&city={}&industry=&position='.format(self.spiderContent['kind'], self.spiderContent['base'])
        #     self.meta = self.getProxy()
        #     self.myCookie = getCookie()
        #     yield scrapy.Request(url=requestUrl, callback=self.parse, meta=self.meta, dont_filter=True)
        # else:
        # employItems = response.css('.job-list>ul>li')
        employItems = response.xpath('//div[@class="job-list"]/ul/li')
        nextPageUrl = response.xpath('//a[@ka="page-next"]/@href').extract_first()
        # self.logger(response.body)
        kind = response.xpath('//input[@class="ipt-search"]/@value').extract_first()
        print('employItems', employItems.extract_first())
        for item in employItems:
            spiderItem = SpiderItem()
            spiderItem['base'] = item.css('p::text').extract_first()[0:2]
            spiderItem['company'] = item.css('.company-text>.name>a::text').extract_first()
            spiderItem['position'] = item.css('.job-title::text').extract_first()
            spiderItem['minPayment'] = item.css('.red::text').extract_first()[0:2]
            spiderItem['maxPayment'] = item.css('.red::text').extract_first()[3:6]
            spiderItem['eduBg'] = item.css('p::text').extract()[2]
            spiderItem['updateTime'] = item.css('.info-publis>p::text').extract_first()[3:]
            spiderItem['updateMonth'] = item.css('.info-publis>p::text').extract_first()[3:5]
            spiderItem['kind'] = kind
            yield spiderItem
        if nextPageUrl != 'javascript:;':
            time.sleep(random.randrange(1, 4))
            next_page = response.urljoin(nextPageUrl)
            # 回调parse处理下一页的url
            yield scrapy.Request(next_page, callback=self.parse, cookies=self.myCookie['dictCookie'], dont_filter=True)

        else:
            print('~~~~~OVER一组~~~~')
            print(self.baseListIndex, self.kindListIndex)
            print('~~~~~~~')
            if self.baseListIndex == 8 and self.kindListIndex != 3:
                print('--------改行------')
                self.kindListIndex += 1
                self.baseListIndex = 0
                self.spiderContent['kind'] = self.kindList[self.kindListIndex]
                self.spiderContent['base'] = self.baseList[self.baseListIndex].values()[0]
                requestUrl = 'https://www.zhipin.com/job_detail/?query={}&city={}&industry=&position='.format(self.spiderContent['kind'], self.spiderContent['base'])
                time.sleep(random.randrange(1, 4))
                yield scrapy.Request(url=requestUrl, callback=self.parse, cookies=self.myCookie['dictCookie'], dont_filter=True)
            elif self.baseListIndex == 8 and self.kindListIndex == 3:
                print('OVER!!!')
            else:
                print('------换地方啊--------------')
                self.baseListIndex +=1
                self.spiderContent['kind'] = self.kindList[self.kindListIndex]
                self.spiderContent['base'] = self.baseList[self.baseListIndex].values()[0]
                time.sleep(2)
                yield scrapy.Request('https://www.zhipin.com', callback=self.parse, cookies=self.myCookie['dictCookie'], dont_filter=True)





