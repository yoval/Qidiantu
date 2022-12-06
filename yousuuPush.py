# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 06:14:34 2022

@author: Administrator
"""
import requests

bookUrl = 'https://book.qidian.com/info/1033991158/'

QidianUrl = 'https://book.qidian.com/info/1034250103/'
Conn = requests.session()
loginUrl = 'https://api.yousuu.com/api/login'
loginData = {'password': "",'userName': "492119549@qq.com"}
loginResp = Conn.post(loginUrl,loginData)
print(loginResp.json()['message'])

pushUrl = 'https://api.yousuu.com/api/crawler'
pushData = {'url': pushUrl}
pushReap = Conn.post(pushUrl,bookUrl)