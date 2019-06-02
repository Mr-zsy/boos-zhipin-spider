import random

cookies = [
"lastCity=101010100; __c=1559469491; __g=-; __l=l=%2Fwww.zhipin.com%2F%3Fka%3Dheader-home&r=https%3A%2F%2Fwww.zhipin.com%2Fgeek%2Fnew%2Findex%2Fresume; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1559203861; t=nPUbV1b1jhI3wiFs; wt=nPUbV1b1jhI3wiFs; JSESSIONID=h4E0g_8KNrBgE1-5gw47GQhp6c9167ePANOTX5u2; __a=47132561.1559469494.1559469494.1559469491.2.2.2.2; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1559471338"
]


def getStrCookie():
    return random.choice(cookies)


def getCookie():
    dictCookie = {}
    strCookie = getStrCookie()
    arrCookie = strCookie.split(';')
    for cookie in arrCookie:
        key = cookie.split('=', 1)[0]
        value = cookie.split('=', 1)[1]
        dictCookie[key] = value
    print('dictCookie', dictCookie)
    return {
        "dictCookie":dictCookie,
        "strCookie":strCookie
    }