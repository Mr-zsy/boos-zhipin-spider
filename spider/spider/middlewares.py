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
from spider.spider.proxy.database import RedisClient
from scrapy.utils.project import get_project_settings
import requests
import json
import re
import time

# class LoginMiddleWare(object):
#     def process_request(self, request, spider):
#         if not spider.loginStatus :
#             try:
#                 browser = spider.browser
#                 browser.get(request.url)
#             except TimeoutException:
#                 print("请求页面超时！！")
#                 return HtmlResponse(url=request.url, status=500, request=request)
#             self.userLogin(browser)
#             spider.loginStatus = True
#             response = browser.page_source
#             return HtmlResponse(url=request.url, body=response, encoding='utf-8', request=request)
#
#     # 登录
#     @classmethod
#     def userLogin(cls, browser):
#         mySetting = get_project_settings()
#         indexLoginBtn = browser.find_element_by_xpath("//a[@ka='header-login']")
#         indexLoginBtn.click()
#         accountIpt = browser.find_element_by_xpath("//input[@name='account']")
#         passwordIpt = browser.find_element_by_xpath("//input[@name='password']")
#         slider = browser.find_element_by_css_selector('.btn_slide')
#         loginBtn = browser.find_element_by_css_selector('.btn')
#         accountIpt.send_keys(mySetting.get('USER_NAME'))
#         passwordIpt.send_keys(mySetting.get('USER_PASSWORD'))
#         ActionChains(browser).click_and_hold(slider).perform()
#         tracks = cls.get_track(280)
#         for x in tracks:
#             ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
#         time.sleep(0.5)
#         ActionChains(browser).release().perform()
#         time.sleep(1)
#         loginBtn.click()
#
#     # 获取轨迹
#     @classmethod
#     def get_track(cls, distance):
#         # 移动轨迹
#         track = []
#         # 当前位移
#         current = 0
#         # 减速阈值
#         mid = distance * 4 / 5
#         # 计算间隔
#         t = 0.2
#         # 初速度
#         v = 0
#
#         while current < distance:
#             if current < mid:
#                 a = 2
#             else:
#                 a = -3
#             v0 = v
#             v = v0 + a * t
#             move = v0 * t + 1 / 2 * a * t * t
#             current += move
#             track.append(round(move))
#         return track
class LoginMiddleWare(object):

    def process_request(self, request, spider):
        if not spider.loginStatus :
            try:
                browser = spider.browser
                browser.get(request.url)
            except TimeoutException:
                print("请求页面超时！！")
                return HtmlResponse(url=request.url, status=500, request=request)
            self.userLogin(browser, spider)
            spider.loginStatus = True
            return HtmlResponse(url=request.url, body=spider.browser.page_source, encoding='utf-8', request=request)
    # 登录
    @classmethod
    def userLogin(cls, browser, spider):
        mySetting = get_project_settings()
        indexLoginBtn = browser.find_element_by_xpath("//a[@ka='header-login']")
        indexLoginBtn.click()
        qrCode = browser.find_element_by_css_selector('.link-scan')
        qrCode.click()
        loginBtn = browser.find_element_by_css_selector('.btn')
        print('''
            **************************
            *    请使用app扫码登录     *
            **************************
        ''')

        previewBtn = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.prv-view-btn')))
        home = browser.find_element_by_xpath("//a[@ka='header-home']")

        home.click()




class ProxyMiddleWare(object):

    def __init__(self):
        self.proxy = RedisClient().pop_proxy().decode("utf8")

    @classmethod
    def getProxy(cls):
        proxy = requests.get('http://127.0.0.1:3289/pop')
        proxy_json = json.loads(proxy.text)
        return proxy_json.get('http', proxy_json.get('https'))

    def process_request(self, request, spider):

        request.meta['proxy'] = self.getProxy()

    def process_response(self, request, response, spider):

        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            self.proxy = RedisClient().pop_proxy().decode("utf8")
            print("response not 200:" + self.proxy)

            # 请求代理池，随即返回一个代理
            request.meta['proxy'] = self.getProxy()
            # request.meta['proxy'] = self.proxy
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

        if request.url == "https://www.zhipin.com" :
        # print(request.url)
        # if re.match("https://www.zhipin.com", request.url ) != None:

            print('~~~~~翻页~~~')
            base = spider.spiderContent['base']
            kind = spider.spiderContent['kind']
            print('request.meta funck',request.meta)
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
                    # spider.ipError = True
                    return request
            except NoSuchElementException:
                response = browser.page_source
                return HtmlResponse(url=request.url, body=response, encoding='utf-8', request=request)
        return  HtmlResponse(url=request.url, body=browser.page_source, encoding='utf-8', request=request)



