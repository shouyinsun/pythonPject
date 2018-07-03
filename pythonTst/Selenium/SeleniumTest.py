from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  # 导入Keys
import time

driver = webdriver.Chrome()  # 指定使用的浏览器
driver.get("http://www.python.org")  # 请求网页地址
assert "Python" in driver.title  # 看看Python关键字是否在网页title中
elem = driver.find_element_by_name("q")  # 找到name为q的元素,这里是个搜索框
elem.clear()  # 清空搜索框中的内容
elem.send_keys("cash")  # 在搜索框中输入
elem.send_keys(Keys.RETURN)  # 相当于回车键,提交
time.sleep(10)
assert "No results found." not in driver.page_source  # 如果当前页面文本中有“No results found.”则程序跳出
time.sleep(100)
driver.close()  # 关闭webdriver
