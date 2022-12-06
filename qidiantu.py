# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 04:33:41 2022

@author: Administrator

"""
from xpinyin import Pinyin
from bs4 import BeautifulSoup
import requests,calendar,re,time,datetime,json

year = 2022
month = 7
checkTag = '仙侠'

Nowday = time.strftime("%Y-%m-%d", time.localtime())
yesterday = datetime.date.today() + datetime.timedelta(-1)
Yesterday = '%s-%s-%s'%(yesterday.year,str(yesterday.month).rjust(2,'0'),str(yesterday.day).rjust(2,'0'))
bookList = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
tagDic = {'首页':1,'玄幻':2,'奇幻':3,'武侠':4,'仙侠':5,'都市':6,'现实':7,'军事':8,'历史':9,'游戏':10,'体育':11,'科幻':12,'悬疑':13,'轻小说':14,'短篇':26,'诸天无限':27}
dayList = range(calendar.monthrange(year, month)[1]+1)[1:]
for day in dayList:
    date = '%s-%s-%s'%(year,month,day)
    bangUrl = 'https://www.qidiantu.com/bang/%s/%s'%(tagDic[checkTag],date)
    resp = requests.get(bangUrl,headers = headers)
    html = resp.text
    bookUrlList = re.findall('href="(/info/.*?/d)"', html)
    bookUrlList = list(set(bookUrlList))
    bookUrlList = ['https://www.qidiantu.com'+i for i in bookUrlList]
    bookUrlList = [i[:-2] for i in bookUrlList]
    for bookUrl in bookUrlList:
        time.sleep(1)
        bookResp = requests.get(bookUrl,headers = headers)
        bookSoup = BeautifulSoup(bookResp.text,'lxml')
        BookName = bookSoup.h1.text
        print(BookName)
        Author = bookSoup.select('body > div.container > div > div.col-sm-10 > div.well.well-sm.table-responsive > table > tbody > tr > td > div > div.media-body > table > tbody > tr:nth-child(1) > td > a:nth-child(3)')[0].text
        RefreshDay = bookSoup.select('body > div.container > div > div.col-sm-10 > div.well.well-sm.table-responsive > table > tbody > tr > td > div > div.media-body > table > tbody > tr:nth-child(5) > td')[0].text
        RefreshDay = RefreshDay.replace('\u3000','')
        RefreshDay = RefreshDay.replace('刷新时间:','')
        introduction = bookSoup.select('body > div.container > div > div.col-sm-10 > div:nth-child(5) > div')[0].text
        if Yesterday in RefreshDay or  Nowday in RefreshDay :
            book = {"author":Author,'intro':introduction,'name':BookName}
            bookList.append(book)
#        break
#    break
p = Pinyin() 
pyName = p.get_pinyin(checkTag,'')
FileName = pyName +'_' + '%s-%s'%(year,month)
with open('%s.json'%FileName,'w',encoding='utf-8') as f:
    json.dump(bookList,f,ensure_ascii=False,indent = 2)