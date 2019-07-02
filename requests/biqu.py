#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup as bs
import re
from retrying import retry
class BiQu(object):
    def __init__(self):
        self.headers={
            'Connection': 'Close',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3783.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.help=Helper()
    @retry(stop_max_attempt_number=3)  # 最大重试3次，3次全部报错，才会报错
    def _parse_url(self,url):
        response = requests.get(url, headers=self.headers, timeout=15)  # 超时的时候回报错并重试
        assert response.status_code == 200  # 状态码不是200，也会报错并充实
        return response

    def parse_url(self,url):
        try:  # 进行异常捕获
            response = self._parse_url(url)
        except Exception as e:
            print(e)
            response = None
        return response
    def spider(self,url):
        response=self._parse_url(url)
        try:
            soup=bs(response.text,"lxml")
            tag_dl = soup.find_all('dl')
            for tag_dd in tag_dl:
                name=tag_dd.find('h3').find('a').get_text()
                summary=tag_dd.find('dd',attrs={'class':'book_des'}).get_text()
                author=tag_dd.find_all('dd',attrs={'class':'book_other'})[0].find('span').get_text()
                new_url=tag_dd.find('h3').find('a').get('href')
                id=new_url[new_url.find('book/')+4:].strip('/')
                self.help.Insert_fiction_name(id,name,author,new_url,summary)
                self.spider_article_url(new_url)
            #翻页
            tag_next = soup.find_all('a',attrs={'class':'next'})
            next_url=tag_next[-1].get('href')
            self.spider(next_url)
        except Exception as e:
            print('spider:'+e)
    def spider_article_url(self,url):
        response = self._parse_url(url)
        try:
            soup=bs(response.text,'lxml')
            id = url[url.find('book/') + 4:].strip('/')
            tags=soup.find('div',attrs={'class':'book_list'}).find_all('li')
            content_list = []
            for tag in tags:
                # content += tag.find('a').get_text().strip('\n').replace('\'','
                new_url = url + tag.find('a').get('href')
                list = self.spider_content(new_url)
                new_id = new_url.split('/')[-1]
                pattern = re.compile(r'[0-9]+')
                nid = pattern.findall(new_id)[0]
                content_list.append((nid,id,list[0],list[1],url))
                if len(content_list)==60:
                    #INSERT
                    content_list=[]
            if content_list!=[]:
                #INSERT
        except Exception as e:
            print('spider_article_url:'+e)
    def spider_content(self,url):
        response = self._parse_url(url)
        try:
            soup=bs(response.text,'lxml')
            content = soup.find('div',attrs={'class':'contentbox clear'}).get_text().strip(' ').replace('\'','')
            title=soup.find('h1').get_text()
            return [title,content]
        except Exception as e:
            print('spider_content:'+e)
            return ['','']
if __name__=="__main__":
    print('启动爬虫！')
    biqu=BiQu()
    start_url = 'http://www.biquw.com/xs/'
    biqu.spider(start_url)
    print('爬虫结束！')
