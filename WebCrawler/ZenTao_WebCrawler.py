#!/usr/bin/python3
# coding=utf-8


from bs4 import BeautifulSoup
import requests

import sys
import argparse
import time

huihuSession = requests.session()

def login():
    URL = "http://192.168.1.40/zentao/user-login-aHR0cDovLzE5Mi4xNjguMS40MC96ZW50YW8vY29tcGFueS1lZmZvcnQtYWxsLmh0bWw=.html"
    header = {
        "Connection":"keep-alive",
        "Content-Length":"167",
        "Cache-Control":"max-age=0",
        "Origin":"http://192.168.1.40",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://192.168.1.40/zentao/user-login-aHR0cDovLzE5Mi4xNjguMS40MC96ZW50YW8vY29tcGFueS1lZmZvcnQtYWxsLmh0bWw=.html",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cookie":"lang=zh-cn; device=desktop; keepLogin=on; za=wangzhi; theme=green; pagerCompanyBrowse=500; ajax_lastNext=on; preProjectID=43; lastProject=30; zp=596c64ad5f18683f3f87357ed07891f6d36100c0; windowWidth=1239; windowHeight=696; zentaosid=1t7hbuto4jpu3c0l0hh9neoea1",
    }

    postData = {
        "account":"wangzhi",
        "password":"ac529fb2469ba1589c10a4cafbda7554",
        "keepLogin[]":"on",
        "referer":"http://192.168.1.40/zentao/company-effort-all.html",
        "verifyRand":"2004027898",
    }

    print("Login...")
    responseRes = huihuSession.post(URL, data = postData, headers = header, allow_redirects = False)
    soup = BeautifulSoup(responseRes.content, 'html.parser')
    print(soup)

def getname(name):
    URL = "http://192.168.1.40/zentao/company-browse.html"
    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Cookie":"lang=zh-cn; device=desktop; keepLogin=on; za=wangzhi; theme=green; ajax_lastNext=on; lastProduct=39; preBranch=0; preProductID=39; lastProject=87; pagerCompanyBrowse=500; zp=596c64ad5f18683f3f87357ed07891f6d36100c0; windowWidth=1600; windowHeight=255; zentaosid=1t7hbuto4jpu3c0l0hh9neoea1",
        "Host":"192.168.1.40",
        "Referer":"http://192.168.1.40/zentao/company-browse.html",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }
    
    responseRes = huihuSession.get(URL, headers = header, allow_redirects = False)
    soup = BeautifulSoup(responseRes.content, 'html.parser')
    #print(soup)

    for child in soup.find_all('tr'):
        if name in child.text:
            result = child.find_all('td')[2:3]
            s = str(result[0])
            return s[4:-5]

    return None

def getinfo(department, startday, day, name):
    URL = "http://192.168.1.40/zentao/company-calendar-%d-%d-%d-0-0-%s-0-yes.html" % (department, startday, startday + day * 24 * 60 * 60 - 1, name)
    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Cookie":"lang=zh-cn; device=desktop; keepLogin=on; za=wangzhi; theme=green; ajax_lastNext=on; lastProduct=39; preBranch=0; preProductID=39; lastProject=87; pagerCompanyBrowse=500; zp=596c64ad5f18683f3f87357ed07891f6d36100c0; windowWidth=1600; windowHeight=255; zentaosid=1t7hbuto4jpu3c0l0hh9neoea1",
        "Host":"192.168.1.40",
        "Referer":URL,
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }
    
    responseRes = huihuSession.get(URL, headers = header, allow_redirects = False)
    soup = BeautifulSoup(responseRes.content, 'html.parser')
    #print(soup)

    i = 0
    for child in soup.find_all('td', attrs={'id': 'diary-title'}):
        if (child.find("li") is not None):
            print("----------")
            logtime = time.localtime(startday + i * 24 * 60 * 60)
            print("%d-%d-%d:" % (logtime.tm_year, logtime.tm_mon, logtime.tm_mday))
            for tag in child.find_all('li', attrs={'title': True}):
                print(tag['title'])
        
        i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'ZenTao Log.')
    parser.add_argument('--department', nargs = '*', default = '8')
    parser.add_argument('--checktype', nargs = '*', default = '1')
    parser.add_argument('--name', nargs = '*', default = '0')
    args = vars(parser.parse_args())    
    #print(args)

    department = args['department'][0]
    checktype = args['checktype'][0]
    name = args['name'][0]
    
    ticks = time.time()
    localtime = time.localtime(ticks)
    #print(localtime)

    startdate = 0
    span = 0
    if (int(checktype) == 0):
        #本周
        startdate = ticks - (((((localtime.tm_wday * 24 + localtime.tm_hour) * 60) + localtime.tm_min) * 60) + localtime.tm_sec)
        span = 7
    elif (int(checktype) == 1):
        #本月
        startdate = ticks - ((((((localtime.tm_mday - 1) * 24 + localtime.tm_hour) * 60) + localtime.tm_min) * 60) + localtime.tm_sec)
        if ((localtime.tm_mon == 1) or (localtime.tm_mon == 3) or (localtime.tm_mon == 5) or (localtime.tm_mon == 7) or (localtime.tm_mon == 8) or (localtime.tm_mon == 10) or (localtime.tm_mon == 12)) :
            span = 31
        elif ((localtime.tm_mon == 4) or (localtime.tm_mon == 6) or (localtime.tm_mon == 9) or (localtime.tm_mon == 11)):
            span = 30
        else:
            if  (((localtime.tm_year % 100 != 0) and (localtime.tm_year % 4 == 0)) or ((localtime.tm_year % 100 == 0) and (localtime.tm_year % 400 == 0))):
                span = 29
            else:
                span = 28

    loginok = False
    if (name == '0'):
        name = "王祉"

    pinyin = getname(name)
    if (pinyin is None):
        login()
        pinyin = getname(name)
        if (pinyin is not None):
            loginok = True
            getinfo(int(department), startdate, span, pinyin)
    else:
        loginok = True

    if (loginok == True):
        print("             ------------")
        print("                 \033[1;31m%s\033[0m" % name)
        print("             ------------")
        if (int(checktype) == 0):
            print("             本周工作日志")
        else:
            print("             本月工作日志")
        getinfo(int(department), startdate, span, pinyin)
