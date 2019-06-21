# -*- coding:utf8-*-
import requests
import time
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytesseract
from PIL import Image
from io import BytesIO
import csv
import xlsxwriter
'''
登陆东方医疗器械网，爬取代理商姓名、省份、联系方式
'''
class DFYLQX:
    def __init__(self):
        self.s = r'token:\'[0-9a-zA-Z]+'
       
        self.url='http://www.qxw18.com/member/login.php'
            
        self.header1 = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.qxw18.com',
            'Origin': 'http://www.qxw18.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3783.0 Safari/537.36',
            'Referer': 'http://www.qxw18.com/daili/',
            'X-Requested-With': 'XMLHttpRequest',
        }
#使用webdriver打开页面实现点击按钮加载图片效果
    def Login_Webdriver(self):
        url = 'http://www.qxw18.com/member/login.php'
        chrome_options = Options()
        # 关闭使用 ChromeDriver 打开浏览器时上部提示语 "Chrome正在受到自动软件的控制"
        chrome_options.add_argument("disable-infobars")
        # 允许浏览器重定向，Framebusting requires same-origin or a user gesture
        chrome_options.add_argument("disable-web-security")
        # 不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式，避免被识别
        chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
        browser = webdriver.Chrome(executable_path="/Users/mac/bin/chromedriver", options=chrome_options)
        browser.get(url)
        username = "***********"
        passwd = "***********"
        browser.implicitly_wait(10)
        elem = browser.find_element_by_name("username")
        elem.send_keys(username)
        elem = browser.find_element_by_name("password")
        elem.send_keys(passwd)
        browser.find_element_by_class_name('button-dl').click()
        num=1
        url='http://www.qxw18.com/daili/'
        while num<600:
            browser.get(url,timeout=10)
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located(((By.CLASS_NAME), 'yeshu')))
            html=browser.page_source
            try:
                soup = BeautifulSoup(html, "lxml")
                table = soup.find('table', attrs={'class': 'dls_name'})
                url_list=browser.find_elements_by_class_name('dls_look')
                tr = table.find_all('tr')
                content = ''
                for i,j in zip(tr[1:],url_list):
                    td = i.find_all('td')
                    content += td[1].text.strip()+'  '
                    content += td[2].text.strip() + '  '
                    content += td[3].text.strip() + '  '
                    j.click()
                    time.sleep(1)
                    img_url=browser.find_element_by_class_name('PLG-dialogBox-content').find_element_by_tag_name('img').get_attribute('src')
                    response = requests.get(img_url)
                    response = response.content
                    BytesIOObj = BytesIO()
                    BytesIOObj.write(response)
                    image = Image.open(BytesIOObj)
                    s = pytesseract.image_to_string(image)
                    pattern = re.compile('[0-9]+')
                    pid_url = pattern.findall(s)
                    content += img_url.strip() + '  '
                    content += str(pid_url)+'\n'
                    browser.find_element_by_class_name('surebtn').click()
                with open('data.txt','a',encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                with open('requestion1.txt','a',encoding='utf-8') as f:
                    f.write(url+'\n')
            list_a=browser.find_element_by_class_name('yeshu').find_elements_by_tag_name('a')
            url=list_a[len(list_a)-1].get_attribute('href')
            num+=1
    def write_csv(self):
        with open('data_1.txt') as f:
            for i in f.readlines():
                l=i.split('  ')
                with open('test.csv','a') as csvfile:
                    writer=csv.writer(csvfile,dialect='excel')
                    writer.writerow([l[0],l[1],l[2],l[3],l[4]])
    def write_excel(self):
        workbook = xlsxwriter.Workbook('kami2.xlsx')  # 创建一个Excel文件
        worksheet = workbook.add_worksheet()  # 创建一个sheet
        with open('data.txt') as f:
            data_list=f.readlines()
            for i in range(len(data_list)):
                l=data_list[i].split('  ')
                num0 = str(i + 1)
                row = 'A' + num0
                data = [l[0],l[1],l[2],l[3],l[4]]
                worksheet.write_row(row,data)
        workbook.close()
if __name__ == "__main__":
    dfylqx = DFYLQX()
    dfylqx.Login_Webdriver()
