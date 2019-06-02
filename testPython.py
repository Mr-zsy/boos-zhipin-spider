from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


def login():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get("http://www.zhipin.com")
    indexLoginBtn = browser.find_element_by_xpath("//a[@ka='header-login']")
    indexLoginBtn.click()
    accountIpt = browser.find_element_by_xpath("//input[@name='account']")
    passwordIpt = browser.find_element_by_xpath("//input[@name='password']")
    slider = browser.find_element_by_css_selector('.btn_slide')
    loginBtn = browser.find_element_by_css_selector('.btn')
    accountIpt.send_keys("18135247181")
    passwordIpt.send_keys("123qwe")
    ActionChains(browser).click_and_hold(slider).perform()
    tracks = get_track(276)
    time.sleep(2)
    for x in tracks:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
        browser.execute_script(f"document.querySelector('#nc_1__bg').style='width:{x}'")
    time.sleep(0.5)
    ActionChains(browser).release().perform()
    time.sleep(1)

    print(browser.get_cookies())

    # loginBtn.click()

def get_track(distance):
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track


if __name__ == "__main__":
    login()
