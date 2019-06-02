import requests
from bs4 import BeautifulSoup
import time
import random
import json
import sys
from bs_spider.user_agent_util import getUserAgent
from bs_spider.cookie_util import getCookie
from selenium import webdriver
from bs_spider.dataClean import DataClean

# https://www.zhipin.com/job_detail/?query=JAVA&city=101100100&industry=&position=
global proxy
kindList = ['Python', "Java", "Web前端", 'C++']
cities = ['101010100', '101020100', '101280100', '101280600', '101210100', '101030100', '101110100', '101270100',
          '101200100']


class Spider:
    def __init__(self):
        self.proxy = self.getProxy()
        self.pageIndex = 0
        self.cookie = getCookie()

    def getProxy(self):
        res = requests.get('http://127.0.0.1:3289/pop')
        global proxy
        proxy = json.loads(res.text)
        ip_port = proxy.get('http', proxy.get('https')).split('://')
        print(ip_port)
        return {ip_port[0]: ip_port[1]}


    def get_cookie(self):
        cookie_dict = {}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.brower = webdriver.Chrome(chrome_options=chrome_options)
        self.brower.get('http://www.zhipin.com')
        cookies_list = self.brower.get_cookies()
        self.brower.close()
        for cookie in cookies_list:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict

    def get_cookie_str(self, cookie_dict):
        res = ""
        for key, value in cookie_dict.items():
            res = res + str(key) + '=' + str(value) + ';'
        return res

    def spiderFunc(self):
        for city in cities:
            for kind in kindList:
                for i in range(1, 6):
                    self.parseUrl(city, kind, i, self.proxy)

    def parseUrl(self, city, kind, i, proxy):
        headers = {
            'User-Agent': getUserAgent(),
            'cookie': self.cookie['strCookie']
        }
        url = f'https://www.zhipin.com/c{city}/?query={kind}&page={i}&ka=page-{i}'
        try:
            response = requests.get(url=url, headers=headers, proxies=proxy, cookies=self.cookie['dictCookie'])
        except Exception as e:
            print('代理服务器无法连接')
            self.proxy = self.getProxy()

            self.parseUrl(city, kind, i, self.proxy)

        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)
        job_list = soup.select('#main>div>div.job-list>ul')
        if not job_list:
            print('被封了')
            self.proxy = self.getProxy()
            self.cookie = getCookie()
            time.sleep(random.randrange(1, 4))
            self.parseUrl(city, kind, i, self.proxy)
        else:
            self.pageIndex += 1
            print('第', self.pageIndex,"页")
            employItems = soup.select('.job-list>ul>li')
            kind = soup.select('input.ipt-search')[0].attrs['value']
            for item in employItems:
                spiderItem = {}
                spiderItem['base'] = item.select('p::text')[0][0:2]
                spiderItem['company'] = item.select('.company-text>.name>a::text')[0]
                spiderItem['position'] = item.select('.job-title::text')[0]
                spiderItem['minPayment'] = item.select('.red::text')[0][0:2]
                spiderItem['maxPayment'] = item.select('.red::text')[0][3:6]
                spiderItem['eduBg'] = item.select('p::text')[2]
                spiderItem['updateTime'] = item.select('.info-publis>p::text')[0][3:]
                spiderItem['updateMonth'] = item.select('.info-publis>p::text')[0][3:5]
                spiderItem['kind'] = kind
                DataClean.dataClean(spiderItem)

            time.sleep(random.randrange(1, 4))


if __name__ == "__main__":
    Spider().spiderFunc()
