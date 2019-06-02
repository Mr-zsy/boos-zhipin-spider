import random

cookies = [

"t=nPUbV1b1jhI3wiFs; wt=nPUbV1b1jhI3wiFs; JSESSIONID=ZcciM7RPN9Ria6prZutT4F2bxQKAOT_gp8iiHm8m; __g=-; __l=%22r=https%3A%2F%2Flogin.zhipin.com%2F%3Fka%3Dheader-login&l=%2Fqrscan%2Fdispatcher%3FqrId%3Dbosszp-26f7f378-d669-4cc9-9d68-48ec6f6d608a%22; __a=98603819.1559463584..1559463584.1.1.1.1; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1559203861; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1559463585"
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