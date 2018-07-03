# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
import logging
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

    def login(self):
        start_time = time.time()
        # r = self.request(self.web_url)
        # 使用selenium通过PhantomJS来进行网络请求
        # driver = webdriver.PhantomJS()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(1120, 600)
        # driver.set_page_load_timeout(load_timeout)
        driver.get(self.web_url)
        driver.save_screenshot("snapshots/home_page.png")

        # link = driver.find_element_by_link_text("Join / Log In")
        link = driver.find_element_by_class_name("join-log-in")
        link.click()
        time.sleep(2)

        driver.save_screenshot("snapshots/modal.png")

        emailInput = driver.find_element_by_name("emailAddress")
        emailInput.clear()
        emailInput.send_keys("442620332@qq.com")

        passwordInput = driver.find_element_by_name("password")
        passwordInput.clear()
        passwordInput.send_keys("Nik3nike")

        loginButton = driver.find_element_by_xpath("//input[@type='button']")
        driver.save_screenshot("snapshots/filled-modal.png")
        print('Login clicked |  sleep for 4 sec. ')

        loginButton.click()
        time.sleep(10)

        driver.save_screenshot("snapshots/inLogin.png")

        end_time = time.time()
        print('consume time:'+str(end_time-start_time))


nikeWeb = NikeWeb()
nikeWeb.login()