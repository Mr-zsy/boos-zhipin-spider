import multiprocessing

# from proxy_pool.flask_web import startProxyPoolApp


from server.web_server import web_app



# if __name__ == '__main__':

# def startProxyApp():
#     # 启动代理池服务端
#     startProxyPoolApp()

def startWebApp():
    #启动web服务端
    web_app.run()

#
# p1 = multiprocessing.Process(target=startProxyApp)
# p2 = multiprocessing.Process(target=startWebApp)
#
#
# p1.start()
# p2.start()
startWebApp()