# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
import requests
import json
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
# from spider.spider.proxy.database import RedisClient
from scrapy.utils.project import get_project_settings
import requests
import json
import re
import time
from spider.spider.cookie_util import getCookie
from spider.spider.user_agent_util import getUserAgent

class RequestMiddleware(object):

    @classmethod
    def getHeaders(cls, spider):
        headers = {
            'User-Agent': getUserAgent(),
            'cookie': spider.myCookie['strCookie']
        }
        print('heasers',headers)
        return headers

    def process_request(self, request, spider):

        requestUrl = 'https://www.zhipin.com/job_detail/?query={}&city={}&industry=&position='.format(spider.spiderContent['kind'], spider.spiderContent['base'])

        while True:
            try:
                print('spider.myProxy',spider.myProxy,)
                response = requests.get(url=requestUrl, headers=RequestMiddleware.getHeaders(spider), proxies=spider.myProxy, cookies=spider.myCookie['dictCookie'])
            except Exception as e:
                print('代理服务器无法连接')
                spider.myProxy = spider.getProxy()
                time.sleep(1)
            else:
                break
        return  HtmlResponse(url=requestUrl, body=response.body, encoding='utf-8', request=request)
    def process_response(self, request, response, spider):
        job_list = response.css('#main > div > div.job-list > ul')
        if not job_list:
            print('has been ban')
            spider.myProxy = spider.getProxy()
            spider.myCookie = getCookie()
            request
        else:
            self.index += 1
            print('you', self.index)








