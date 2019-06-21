# -*- coding:utf8-*-
import execjs
import requests
from bs4 import  BeautifulSoup as bs

def spider():
    '''
    逆向爬取入门,从网络地址https://www.jianshu.com/p/9abe5f713ed6学习整理
    中国土地市场网
    :return:
    '''
    url='http://www.landchina.com/default.aspx?tabid=226'
    session=requests.session()
    response = session.get(url)

    text = response.text
    # f_js = re.findall("javascript\">(.*?)</script>", text)[0]
    file='test.js'
    ctx = execjs.compile(open(file).read())
    location = ctx.call("YunSuoAutoJump")
    second_url = "http://www.landchina.com" + location
    print(second_url)
    _ = session.get(second_url)

    res = session.get(url)
    # print(res.text)
    soup = bs(res.text, "lxml")
    tag=soup.find('table',attrs={'id':'TAB_contentTable'})
    tags=tag.find_all('tr')
    for i in tags[1:]:
        tag_td=i.find_all('td')
        print(tag_td[1].text.strip())
        print(tag_td[2].text.strip())
        print(tag_td[3].text.strip())

if __name__=="__main__":
    spider()
