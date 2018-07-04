# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
import logging

import requests
from selenium import webdriver
import time

from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename='logs/nikeScript.log',level=logging.ERROR)
logger = logging.getLogger('nikeScript')
implicit_wait_time= 25
load_timeout= 60
max_retry= 2


class NikeWeb:
    def __init__(self):  # 类的初始化操作
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                  'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                                  'Connection': 'keep-alive'
                                  }
        self.web_url = "https://www.nike.com/launch/"  # 要访问的网页地址

        self.cart_url = 'https://secure-store.nike.com/us/checkout/html/cart.jsp'

    def login(self):
        start_time = time.time()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(1200, 600)
        driver.set_page_load_timeout(load_timeout)
        driver.get(self.web_url)
        time.sleep(5)
        driver.save_screenshot("snapshots/home_page.png")

        link = driver.find_element_by_class_name("join-log-in")
        link.click()
        time.sleep(5)

        driver.save_screenshot("snapshots/modal.png")

        emailInput = driver.find_element_by_name("emailAddress")
        emailInput.clear()
        emailInput.send_keys("442620332@qq.com")

        passwordInput = driver.find_element_by_name("password")
        passwordInput.clear()
        passwordInput.send_keys("Nik3nike")

        loginButton = driver.find_element_by_xpath("//input[@type='button']")
        driver.save_screenshot("snapshots/filled-modal.png")

        loginButton.click()
        print('Login clicked ... ')
        time.sleep(5)
        driver.save_screenshot("snapshots/inLogin.png")
        login_end_time = time.time()
        print('login time:'+str(login_end_time-start_time))

        cookies = driver.get_cookies();
        x_cookie = {}
        for cookie in cookies:
            # print(cookie['name'], cookie['value'])
            x_cookie[cookie['name']]=  cookie['value']

        addCartUrl='https://secure-store.nike.com/us/services/jcartService/?action=addItem&rt=json&country=US' \
                   '&region=na&lang_locale=en_US&catalogId=1&productId=12389587&qty=1&skuId=22112527'

        # driver.get(addCartUrl)
        # time.sleep(3)
        # driver.save_screenshot('snapshots/addCart.png')

        s = requests.session()
        requests.utils.add_dict_to_cookiejar(s.cookies, x_cookie)

        cartHeader = {
            "accept": "*/*",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "accept-language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/64.0.3282.140 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br"
        }

        r = s.get(addCartUrl, headers=cartHeader)
        print(r.text)

        addCart_end_time = time.time()
        print('add cart time:'+str(addCart_end_time-login_end_time))

        # 购物车中下单
        driver.get(self.cart_url)
        time.sleep(20)
        driver.save_screenshot("snapshots/inCart.png")

        checkOutBtn= driver.find_element_by_id("ch4_cartCheckoutBtn")
        driver.set_window_size(1200, 1200)
        checkOutBtn.click()

        jumpCart_end_time = time.time()
        print('jump cart time:'+str(jumpCart_end_time-addCart_end_time))




        # 安全码
        time.sleep(10)
        driver.save_screenshot("snapshots/checkout.png")
        credit_card_frame = driver.find_element_by_class_name('credit-card-iframe-cvv')
        driver.switch_to.frame(credit_card_frame)
        cvNum = driver.find_element_by_id('cvNumber')
        cvNum.clear()
        cvNum.send_keys("245")
        driver.save_screenshot("snapshots/cvNum.png")
        # 继续下单
        driver.switch_to.default_content()
        continueOrderReviewBtn= driver.find_element_by_xpath("//button[text()='Continue To Order Review']")
        continueOrderReviewBtn.click()
        time.sleep(5)
        driver.save_screenshot("snapshots/order.png")
        placeOrderBtn = driver.find_element_by_xpath("//button[text()='Place Order']")
        placeOrderBtn.click()
        time.sleep(20)
        driver.save_screenshot("snapshots/placeOrder.png")

        end_time = time.time()
        print('consume time:'+str(end_time-start_time))


nikeWeb = NikeWeb()
nikeWeb.login()