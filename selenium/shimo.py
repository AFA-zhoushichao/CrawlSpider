#-*- coding:utf8-*-
import requests
import random
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

'''
登陆石墨账户爬取账户下各个目录下文件目录
'''
class ShiMo:
  def __init__(self):
      pass
  def Login(self):
      url='https://shimo.im/login'
      chrome_options = Options()
      # 关闭使用 ChromeDriver 打开浏览器时上部提示语 "Chrome正在受到自动软件的控制"
      chrome_options.add_argument("disable-infobars")
      # 允许浏览器重定向，Framebusting requires same-origin or a user gesture
      chrome_options.add_argument("disable-web-security")
      browser = webdriver.Chrome(executable_path="/Users/mac/bin/chromedriver",options=chrome_options)
      browser.get(url)
      username = "zhousc5300@163.com"
      passwd = "zhousc5300"
      browser.implicitly_wait(10)
      elem = browser.find_element_by_name("mobileOrEmail")
      elem.send_keys(username)
      elem = browser.find_element_by_name("password")
      elem.send_keys(passwd)
      browser.find_element_by_tag_name('button').click()
      time.sleep(5)
      print(browser.get_cookies())

      with open('tmall.json', 'r', encoding='utf-8') as f:
          listCookies = json.loads(f.read())
      cookie = [item["name"] + "=" + item["value"] for item in listCookies]
      cookiestr = '; '.join(item for item in cookie)
      print(cookiestr)
      # wait = WebDriverWait(browser, 10)
      # wait.until(EC.presence_of_element_located(((By.LINK_TEXT), '我的桌面')))
      # browser.find_element_by_link_text('我的桌面').click()
      # wait = WebDriverWait(browser, 10)
      # wait.until(EC.presence_of_element_located(((By.CLASS_NAME), 'file-name')))
      # filename=browser.find_elements_by_class_name('file-name')
      # for i in filename:
      #   print(i.text)
