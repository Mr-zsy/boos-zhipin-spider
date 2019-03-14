# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from spider.spider.proxy.database import RedisClient
import requests
import json


class ProxyMiddleWare(object):

    def __init__(self):
        self.proxy = RedisClient().pop_proxy().decode("utf8")

    def process_request(self, request, spider):
        # if spider.ipError:
        #     '''对request对象加上proxy'''
        #     print("-------this is request ip----------:" + self.proxy)
        #     request.meta['proxy'] = self.proxy
        proxy = requests.get('http://127.0.0.1:3289/pop')
        proxy_json = json.loads(proxy.text)
        request.meta['proxy'] = proxy_json['proxy']


    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            self.proxy = RedisClient().pop_proxy().decode("utf8")
            print("response not 200:" + self.proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = self.proxy
            return request
        return response


class SelenuimDownloaderMiddleware(object):

    def process_request(self, request, spider):

        try:
            browser = spider.browser
            browser.get(request.url)
        except TimeoutException:
            print("请求页面超时！！")
            return HtmlResponse(url=request.url, status=500, request=request)

        if request.url == "https://www.zhipin.com/" or request.url =="https://www.zhipin.com/?ka=header-home":

            base = spider.spiderContent['base']
            kind = spider.spiderContent['kind']

            baseDict = {
                '北京': 'ul[class="show"]>li[ka="hot-city-101010100"]',
                '上海': 'ul[class="show"]>li[ka="hot-city-101020100"]',
                '广州': 'ul[class="show"]>li[ka="hot-city-101280100"]',
                '深圳': 'ul[class="show"]>li[ka="hot-city-101280600"]',
                '杭州': 'ul[class="show"]>li[ka="hot-city-101210100"]',
                '天津': 'ul[class="show"]>li[ka="hot-city-101030100"]',
                '西安': 'ul[class="show"]>li[ka="hot-city-101110100"]',
                '成都': 'ul[class="show"]>li[ka="hot-city-101270100"]',
                '武汉': 'ul[class="show"]>li[ka="hot-city-101200100"]'
            }

            kindDict = {
                'Python': 'Python',
                "Java": "Java",
                "Web前端": "Web前端",
                'C++': 'C++'
            }
            try:
                # citySelect = browser.find_element_by_css_selector('.city-sel')
                citySelect = spider.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.city-sel')))
                print('----1',citySelect)
            except (NoSuchElementException, TimeoutException) as e:
                citySelect = browser.find_element_by_css_selector('.nav-city-box')
                print('----2', citySelect)

            citySelect.click()

            try:
                actions1 = ActionChains(browser)
                province = spider.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.dorpdown-province>li:nth-of-type(1)')))
                actions1.move_to_element(province).perform()
            except TimeoutException:
                print('province元素加载超时')
                print('~~~',request.url)
                return request

            #base
            try:
                actions2 = ActionChains(browser)
                city = spider.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, baseDict[base])))
                actions2.click(city).perform()
            except TimeoutException:
                print('city元素加载超时')
                print('~~~', request.url)
                return request

            #kind
            positionInput = browser.find_element_by_css_selector('.ipt-search')
            positionInput.send_keys(kindDict[kind])
            searchBtn = browser.find_element_by_css_selector('.btn-search')
            searchBtn.click()
            try:
                errorTip = browser.find_element_by_css_selector('.error-content>.text>h1')
                if errorTip:
                    spider.ipError = True
                    return request
            except NoSuchElementException:
                response = browser.page_source


        return HtmlResponse(url=request.url, body=response, encoding='utf-8', request=request)



