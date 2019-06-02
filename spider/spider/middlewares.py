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

class RandomHeaderMiddleware(object):
    def process_request(self, request, spider):
        print("set header")
        request.headers['User-Agent'] = spider.myUserAgent
        request.headers['cookie'] = spider.myCookie['strCookie']
        print('COOKIE', spider.myCookie)


class ProxyMiddleWare(object):

    def process_request(self, request, spider):
        proxy = spider.myProxy
        print('proxy', proxy)
        request.meta['proxy'] = proxy
        # return HtmlResponse(url=request.url, encoding='utf-8', request=request)

class TestMiddleWare(object):

    def process_response(self, request, response, spider):
        time.sleep(1)
        job_list = response.css('div.job-list')
        if not job_list:
            print('requestURL', request.url)
            print('被封了~',request)
            spider.myProxy = spider.getProxy()
            spider.myCookie = getCookie()
            spider.myUserAgent = getUserAgent()
            request.cookies = spider.myCookie['dictCookie']
            return request
        else:
            print(job_list)
            return  HtmlResponse(url=request.url, body=response.body, encoding='utf-8', request=request)







