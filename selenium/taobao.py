#-*- coding:utf8-*-
import requests
import random
import time
import datetime
from bs4 import BeautifulSoup
import re
from DataCollection.Crawel.Common.MySQL.pymysql_helper import Helper
from DataCollection.Crawel.Tmall.tmall_spider.tmall.code.ProductInformationModels import ProductInformationModels
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool



class Spider(object):
    '''
    微博账号登陆淘宝，可以避开滑块
    搜索美妆类然后进行商品信息的爬取，没有在商品分类目录点击筛选
    -------暂时没有添加验证码登陆-------
    '''
    def __init__(self,cate):
        self.cate=cate
    # 获取产品信息
    def Login_WeiBo(self,search_text):
        try:
            chrome_options = Options()
            # 关闭使用 ChromeDriver 打开浏览器时上部提示语 "Chrome正在受到自动软件的控制"
            chrome_options.add_argument("disable-infobars")
            # 允许浏览器重定向，Framebusting requires same-origin or a user gesture
            chrome_options.add_argument("disable-web-security")
            #添加代理
            # chrome_options.add_argument('--proxy-server=http://ip:port')   ,chrome_options=chrome_options
            driver = webdriver.Chrome(executable_path="/Users/mac/bin/chromedriver")
            driver.get("https://login.taobao.com/member/login.jhtml")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located(((By.CLASS_NAME),'login-switch')))
            button_qu = driver.find_element_by_id("J_Quick2Static")
            button_qu.click()
            driver.find_element_by_class_name("weibo-login").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located(((By.NAME), 'username')))
            driver.find_element_by_name('username').send_keys('********')
            driver.find_element_by_name('password').send_keys('**********')
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located(((By.CLASS_NAME), 'W_btn_g')))
            button = driver.find_element_by_class_name("W_btn_g")
            button.click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located(((By.CLASS_NAME), 'search-combobox-input')))
            driver.find_element_by_class_name('search-combobox-input').send_keys(search_text)
            driver.find_element_by_xpath("//div[@class='search-button']/button").click()
            time.sleep(5)
            self.parse_html(driver)
        except Exception as e:
            print(e.args)
    def parse_html(self,driver):
        soup = BeautifulSoup(driver.page_source, "lxml")
        tags_items = soup.find('div', attrs={'class': 'm-itemlist'})
        ps = Pool(10)
        for tag in tags_items.find('div', attrs={'class': 'items'}).children:
            if tag != '\n':
                #价格
                get_price=tag.find('div', attrs={'class': 'price g_price g_price-highlight'}).get_text().strip()[1:]
                #产品名
                get_name=tag.find('div', attrs={'class': 'row row-2 title'}).get_text().strip()
                #产品链接
                get_url=tag.find('a', attrs={'class': 'pic-link J_ClickStat J_ItemPicA'}).get('href')
                #产品id
                get_pid=tag.find('a', attrs={'class': 'pic-link J_ClickStat J_ItemPicA'}).get('data-nid')
                #location
                get_location=tag.find('div', attrs={'class': 'location'}).get_text().strip()
                #店铺名称
                get_shopName=tag.find('div', attrs={'class': 'shop'}).get_text().strip()
                #图片url
                get_imgUrl=tag.find('img', attrs={'class': 'J_ItemPic img'}).get('data-src')
                # pid,source,productName,url,band,category,imageUrl,dateTime,price,updatePrice
                s=''
                s=get_pid+'+'+get_name+'+'+get_url+'+'+get_shopName+'+'+get_imgUrl+'+'+get_price+'\n'
                with open('data.txt',mode='a',encoding='utf-8') as f:
                    f.write(s)
                models=ProductInformationModels(pid=get_pid,source = 'tm',productName = get_name,url=get_url,band = get_shopName,category='mz',imageUrl = get_imgUrl,dateTime = datetime.datetime.now(),price = get_price,updatePrice=0)
                # self.Record(models)
                ps.apply_async(self.Record, args=(models,))
        ps.close()
        ps.join()
        t = random.randrange(20, 30)
        time.sleep(t)
        try:
            button=driver.find_element_by_xpath("//li[@class='item next']/a")
            button.click()
        except Exception as e:
            driver.quit()
            print('结束')
        self.parse_html(driver)
    if __name__ == '__main__':
    print('启动天猫爬虫')
    l_search=['美妆','电子','母婴']
    for i in range(3):
        Spider(i).Login_WeiBo(l_search[i])






