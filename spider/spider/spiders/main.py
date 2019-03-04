# -*- coding: utf-8 -*-
import scrapy
from spider.spider.items import SpiderItem
from selenium import webdriver
from scrapy.utils.project import get_project_settings
from selenium.webdriver.support.ui import WebDriverWait
import time
from spider.spider.proxy.database import RedisClient


class MainSpider(scrapy.Spider):
    #项目的唯一名字，用来区分不同的爬虫
    name = 'recruitment'
    #允许爬取的域名
    allowed_domains = ['www.zhipin.com']
    #spider启动时爬取的url
    start_urls = ['https://www.zhipin.com/?ka=header-home']
    #对settings中的值进行覆盖
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'spider.spider.middlewares.ProxyMiddleWare':542,
            'spider.spider.middlewares.SelenuimDownloaderMiddleware':543
        }
    }

    def __init__(self):
        #设置参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting.get('SELENIUM_TIMEOUT')
        #初始化chrome
        self.browser = webdriver.Chrome()
        #页面加载超时时间
        self.browser.set_page_load_timeout(self.timeout)
        #元素加载超时时间
        self.wait = WebDriverWait(self.browser, 10)

        self.ipError = False

        self.kindList = ['Python', "Java", "Web前端", 'C++']
        # self.kindList = [ "Web前端", 'C++']
        self.baseList = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '成都', '武汉']
        self.kindListIndex = 0
        self.baseListIndex = 0
        self.spiderContent = {
            'kind':'Python',
            'base':'北京'
        }
        # self.spiderContent = {
        #     'kind': 'Web前端',
        #     'base': '北京'
        # }

        #请求start_urls后返回的响应作为唯一参数传给此函数
    def parse(self, response):
        employItems = response.css('.job-list>ul>li')
        nextPageUrl = response.xpath('//a[@ka="page-next"]/@href').extract_first()

        kind = response.xpath('//input[@class="ipt-search"]/@value').extract_first()
        # print(nextPageUrl)
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
            next_page = response.urljoin(nextPageUrl)
            # 回调parse处理下一页的url
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)

        else:
            print('~~~~~OVER一组~~~~')
            print(self.baseListIndex, self.kindListIndex)
            print('~~~~~~~')
            if self.baseListIndex == 8 and self.kindListIndex != 3:
                print('--------改行------')
                self.kindListIndex += 1
                self.baseListIndex = 0
                self.spiderContent['kind'] = self.kindList[self.kindListIndex]
                self.spiderContent['base'] = self.baseList[self.baseListIndex]
                time.sleep(1)
                yield scrapy.Request('https://www.zhipin.com/?ka=header-home', callback=self.parse, dont_filter=True)
            elif self.baseListIndex == 8 and self.kindListIndex == 3:
                print('OVER!!!')
            else:
                print('------换地方啊--------------')
                self.baseListIndex +=1
                self.spiderContent['kind'] = self.kindList[self.kindListIndex]
                self.spiderContent['base'] = self.baseList[self.baseListIndex]
                time.sleep(2)
                yield scrapy.Request('https://www.zhipin.com/?ka=header-home',callback=self.parse, dont_filter=True)





