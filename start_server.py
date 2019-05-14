import multiprocessing

from proxy_pool.async_proxy_pool.proxy_pool_webapi_flask import proxy_app
from proxy_pool.async_proxy_pool.config import SERVER_HOST, SERVER_PORT, SERVER_ACCESS_LOG

from server.web_server import web_app

from spider.spider.startSpider import startSpider



# if __name__ == '__main__':

def startProxyApp():
    # 启动代理池服务端
    proxy_app.run(host=SERVER_HOST, port=SERVER_PORT, debug=SERVER_ACCESS_LOG)

def startWebApp():
    #启动web服务端
    web_app.run()

p1 = multiprocessing.Process(target=startProxyApp)
p2 = multiprocessing.Process(target=startWebApp)
p3 = multiprocessing.Process(target=startSpider)

p1.start()
p2.start()
p3.start()