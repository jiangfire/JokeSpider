import urllib.request
import time
import logging
from bs4 import BeautifulSoup
import sqldb

#Version: 0.1
#Author: JiangFire
#It's ugly but it can run well. I use it to get 3.8mb joke.
#It all in sqliteDB file
#Time: 2016/2/22

#TODO It should in a file not in here
logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S')
logging.basicConfig(level=logging.ERROR,  
                    format='%(asctime)s %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='error.log',  
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
fmt = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(fmt)
logging.getLogger().addHandler(console)

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agaent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agaent }
        self.stories = []
        self.enable = False
        self.conn = sqldb.connectDb()

    def __getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            if hasattr(e, "reason"):
                logging.error("faild:"+e.reason)
                return

    def __getPageItems(self, pageIndex):
        pageCode = self.__getPage(pageIndex)        
        pageStories = []
        funnycount = 1
        temp = ""
        if not pageCode:
            logging.error("Fetch the page faild...")
            return
        logging.info("页面获取成功...开始解析")
        qiusoup = BeautifulSoup(pageCode, "lxml")
        articletag = qiusoup.findAll('div', class_ = 'article block untagged mb15')
        for content in articletag: #get the page, find without picture
            if not content.findAll("div", class_="thumb"):
                for divcontenttag in content.findAll("div", class_="content"):
                    for string in divcontenttag.strings: # a line is a string, not all string is a string
                        temp = temp + string
                    logging.info("这是第%d个......" % funnycount)
                    pageStories.append(temp)
                    temp = ""
                    funnycount = funnycount + 1
        return pageStories
    
    def __loadPage(self):
        if self.enable == True:            
            pageStories = self.__getPageItems(self.pageIndex)
            if pageStories:
                for story in pageStories:
                    self.stories.append(story)
                self.pageIndex += 1
                logging.info("休息一下，准备爬第%s页" % self.pageIndex)
        
    def __storeFunny(self):
        for string in self.stories:
            sqldb.insertData(self.conn, string)
        sqldb.CConn(self.conn)

    def start(self):
        logging.info("正在获取糗事百科笑话...")
        self.enable = True
        while self.pageIndex <= 35:
            self.__loadPage()        
            self.__storeFunny()
            time.sleep(240)
        sqldb.CConn(self.conn, close=True)

if __name__ == '__main__':
    qs = QSBK()
    qs.start()
    
    
