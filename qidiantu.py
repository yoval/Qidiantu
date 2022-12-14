# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 04:33:41 2022

@author: Administrator

"""
from xpinyin import Pinyin
from bs4 import BeautifulSoup
import requests,calendar,time,datetime,json


def run(year,month,checkTag):
    Nowday = time.strftime("%Y-%m-%d", time.localtime())
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    Yesterday = '%s-%s-%s'%(yesterday.year,str(yesterday.month).rjust(2,'0'),str(yesterday.day).rjust(2,'0'))
    BOOKURLLIST = []
    bookList = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    tagDic = {'首页':1,'玄幻':2,'奇幻':3,'武侠':4,'仙侠':5,'都市':6,'现实':7,'军事':8,'历史':9,'游戏':10,'体育':11,'科幻':12,'悬疑':13,'轻小说':14,'短篇':26,'诸天无限':27}
    dayList = range(calendar.monthrange(year, month)[1]+1)[1:]
    for day in dayList:
        date = '%s-%s-%s'%(year,month,day)
        print('正在获取%s的%s类推荐'%(date,checkTag))
        bangUrl = 'https://www.qidiantu.com/bang/%s/%s'%(tagDic[checkTag],date)
        resp = requests.get(bangUrl,headers = headers)
        soup = BeautifulSoup(resp.text,'lxml')
        BookUrlList = soup.select('tbody > tr > td:nth-child(2) > a')
        BookUrlList = [i.get('href') for i in BookUrlList]
        BookUrlList = list(set(BookUrlList))
        BookUrlList = ['https://www.qidiantu.com'+i for i in BookUrlList]
        BookUrlList = [i[:-2] for i in BookUrlList]
        BOOKURLLIST = BOOKURLLIST+BookUrlList
    BOOKURLLIST = list(set(BOOKURLLIST))
    print('%s年%s月份共有%s本书上了%s推荐'%(year,month,len(BOOKURLLIST),checkTag))
    print('即将检测这些书籍最近更新状况……')
    
    for bookUrl in BOOKURLLIST:
        time.sleep(1)
        bookResp = requests.get(bookUrl,headers = headers)
        bookSoup = BeautifulSoup(bookResp.text,'lxml')
        BookName = bookSoup.h1.text
        Author = bookSoup.select('body > div.container > div > div.col-sm-10 > div.well.well-sm.table-responsive > table > tbody > tr > td > div > div.media-body > table > tbody > tr:nth-child(1) > td > a:nth-child(3)')[0].text
        RefreshDay = bookSoup.select('body > div.container > div > div.col-sm-10 > div.well.well-sm.table-responsive > table > tbody > tr > td > div > div.media-body > table > tbody > tr:nth-child(5) > td')[0].text
        RefreshDay = RefreshDay.replace('\u3000','')
        RefreshDay = RefreshDay.replace('刷新时间:','')
        status = bookSoup.select('body > div.container > div > div.col-sm-10 > div.well.well-sm.table-responsive > table > tbody > tr > td > div > div.media-body > table > tbody > tr:nth-child(2) > td')[0].text
        introduction = bookSoup.select('body > div.container > div > div.col-sm-10 > div:nth-child(5) > div')[0].text
        introduction = introduction.replace('展开更多简介 / 收起','')
        if '完结' in status:
            introduction = '已完结\n' + introduction
        if Yesterday in RefreshDay or  Nowday in RefreshDay or '完结' in status:
            print('《%s》,近两日有更新或已完结！'%BookName)
            book = {"author":Author,'intro':introduction,'name':BookName}
            bookList.append(book)
        else:
            print('《%s》,太监了~'%BookName)
    #    break
    print('检测有%s本书已完结最近有更新，即将加入书单！'%len(bookList))
    p = Pinyin() 
    pyName = p.get_pinyin(checkTag,'')
    FileName = pyName +'_' + '%s-%s'%(year,month)
    with open('%s.json'%FileName,'w',encoding='utf-8') as f:
        json.dump(bookList,f,ensure_ascii=False,indent = 2)
    print('已生成书单文件！')

if __name__ == '__main__':
    year = 2022
    month = 1
    checkTag = '科幻'
    for month in [1,2,3,4,5,6]:
        run(year,month,checkTag)
