# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 06:14:34 2022

@author: Administrator
"""
import requests,re


#检测优书是否有次书籍
def Check(bookName):
    params = {
        'type': 'title',
        'value': bookName,
        'page': '1',
        'highlight': '1',
        'from': 'search',
    }
    response = requests.get('https://api.yousuu.com/api/search', params=params,)
    if response.json()['data']['total'] ==0:
        print('无搜索结果')
        return 0
    elif response.json()['data']['total'] >0:
         bookname = response.json()['data']['books'][0]['title']
         bookname = bookname.replace('<em>','')
         bookname = bookname.replace('</em>','')
         if bookname==bookName:
             bookId = response.json()['data']['books'][0]['bookId']
             print('优书网已有此书')
             return bookId
         else:
             print('优书网没有此书')
             return 0
#登录优书网
def loginYousuu():
    loginUrl = 'https://api.yousuu.com/api/login'
    Conn = requests.session()
    loginData = {'password': "****",'userName': "492119549@qq.com"}
    loginResp = Conn.post(loginUrl,loginData)
    print(loginResp.json()['message'])
    return Conn
#添加至“养肥待看”
def addFavs(Conn,qidiantuUrl):
    global pushReap
    bookId = re.findall('\d+',qidiantuUrl)[0]
    qidianUrl = 'https://book.qidian.com/info/'+bookId
    pushUrl = 'https://api.yousuu.com/api/crawler'
    pushData = {'url': qidianUrl}
    pushReap = Conn.post(pushUrl,pushData)
    if pushReap.json()['success'] == 1:
        print('推送至优书网成功！')
        yousuuId = pushReap.json()['data']['bookId']
        Post_resp = Conn.post('https://api.yousuu.com/api/book/addFavs',json={"bookIds":[yousuuId,],"caseId":2})
        if Post_resp.json()['success'] ==1:
            print('添加至“养肥待看”成功！')
            
def add_Favs(Conn,yousuuId):
    Post_resp = Conn.post('https://api.yousuu.com/api/book/addFavs',json={"bookIds":[yousuuId,],"caseId":2})
    if Post_resp.json()['success'] ==1:
        print('添加至“养肥待看”成功！')
        
if __name__=='__main__':
    Conn = loginYousuu()
#    qidiantuUrl = 'https://www.qidiantu.com/info/1035741573'
#    addFavs(Conn,qidiantuUrl)