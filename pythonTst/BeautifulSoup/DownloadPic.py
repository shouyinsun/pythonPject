# !/usr/bin/env python3
#  -*- coding: utf-8 -*-


# 抓取 https://unsplash.com 中的图片
import threadpool as threadpool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pip._vendor import requests
from bs4 import BeautifulSoup
import os
import time


class BeautifulPicture:

    def __init__(self):  # 类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}  # 给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://unsplash.com'  # 要访问的网页地址
        self.folder_path = 'D:\BeautifulPicture'  # 设置图片要存放的文件目录

    def get_pic(self):
        start_time = time.time()
        # r = self.request(self.web_url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(self.web_url)
        self.scroll_down(driver=driver, times=20)  # 执行网页下拉到底部操作
        print('开始获取所有img标签')
        # all_img = BeautifulSoup(r.text, 'lxml').find_all('img', class_='KW7g_ _1hz5D')
        all_img = BeautifulSoup(driver.page_source, 'lxml').find_all('img', class_='_2zEKz')
        print("----------------- the num is:", len(all_img))
        is_new_folder=self.mkdir(self.folder_path)  # 创建文件夹
        os.chdir(self.folder_path)   # 切换到创建的文件夹

        file_names = self.get_files(self.folder_path)  # 获取文件家中的所有文件名,类型是list

        task_pool=threadpool.ThreadPool(10)# 线程池

        for img in all_img:
            img_str = img['src']
            # first_pos = img_str.index('"') + 1
            # second_pos = img_str.index('"', first_pos)
            # img_url = img_str[first_pos: second_pos] #
            img_url = img_str
            # 获取高度和宽度的字符在字符串中的位置
            width_pos = img_url.index('&w=')
            height_pos = img_url.index('&q=')
            width_height_str = img_url[width_pos: height_pos]
            img_url_final = img_url.replace(width_height_str, '')
            # 截取url中参数前面、网址后面的字符串为图片名
            try:
                name_start_pos = img_url.index('photo')
            except ValueError:
                print("Error: 不能解析图片名称")
            else:
                name_end_pos = img_url.index('?')
                img_name = img_url[name_start_pos: name_end_pos]
                # self.save_img(img_url_final, img_name)
                if is_new_folder:
                    # self.save_img(img_url, img_name)
                    requests=threadpool.makeRequests(self.save_img,[((img_url_final,img_name), {})])
                    [task_pool.putRequest(req) for req in requests]
                else:
                    if img_name not in file_names:
                        # self.save_img(img_url, img_name)
                        requests=threadpool.makeRequests(self.save_img,[((img_url_final,img_name), {})])
                        [task_pool.putRequest(req) for req in requests]
                    else:
                        print("该图片已经存在：", img_name, ",不再重新下载。")

        task_pool.wait()

        print('--------------- %d second' % (time.time()-start_time))

    def save_img(self, url, name):
        img = self.request(url)
        file_name = name + '.jpg'
        f = open(file_name, 'ab')
        f.write(img.content)
        f.close()

    def request(self, url):
        r = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求,返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            print(path, '文件夹已经存在了,不再创建')
            return False

    def scroll_down(self, driver, times):  # 下拉
        for i in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 执行JavaScript实现网页下拉倒底部
            print("第", str(i + 1), "次下拉操作执行完毕")
            print("第", str(i + 1), "次等待网页加载......")
            time.sleep(1)  # 等待x秒,页面加载出来再执行下拉操作

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names


beauty = BeautifulPicture()
beauty.get_pic()
