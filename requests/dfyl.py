# -*- coding:utf8-*-
import requests
from bs4 import BeautifulSoup
import re
'''
登陆东方医疗器械网
'''
class DFYLQX:
    def __init__(self):
        self.s = r'token:\'[0-9a-zA-Z]+'
        self.login_data = {
            'forward': 'http://www.qxw18.com/',
            'option': '****',
            'username': '*******',
            'password': '*******',
            'submit': '登录'
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.qxw18.com',
            'Origin': 'http://www.qxw18.com',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3783.0 Safari/537.36',
            'Referer': 'http://www.qxw18.com/member/login.php',
        }
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
        self.url='http://www.qxw18.com/member/login.php'


    def login(self):
        session = requests.session()
        content = session.post(self.url, headers=self.headers, data=self.login_data)
        # print(content.text)
        content1=session.post('http://www.qxw18.com/daili/',headers=self.headers)
        html=content1.text
        # print(html)
        soup = BeautifulSoup(html, "lxml")
        pattern = re.compile(self.s)
        pid_url = pattern.findall(html)
        token=pid_url[0][7:]
        print(token)
        table=soup.find('table',attrs={'class':'dls_name'})
        tr = table.find_all('tr')
        for i in tr[1:]:
            td = i.find_all('td')
            itemid=td[6].find('a').get('rel')[0]
            print(itemid)
            url = 'http://www.qxw18.com/ajax.php?action=buy&op=view'
            post_data = {
                itemid: itemid,
                token: token
            }
            response = session.post(url, post_data, headers=self.header1,cookies=session.cookies)
            print(response.status_code)
            if response.status_code == 200:
                print(response.content)
if __name__ == "__main__":
    dfylqx = DFYLQX()
    dfylqx.login()
