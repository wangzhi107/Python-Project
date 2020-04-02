#!/usr/bin/python3
# coding=utf-8

import requests
import re
import json

huihuSession = requests.session()

def login():
    postUrl = "http://192.168.43.2/erp/php/erpfs.php?action=LoginCheck&time=Mon%20Sep%2030%202019%2009:37:07%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"
    
    postData = {
        "logintype":"email",
        "loginid":"wangzhi@crearo.com",
        "department":"18",
        "cktime":"31536000000",
        "hexpassword":"c639a0e6d07450815dc0938230a197a4",
    }
    
    header = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Content-Length":"123",
        "Content-Type":"application/x-www-form-urlencoded",
        "Cookie":"CR_ERP_NavMenuID=CR_ERP_Employee; CR_ERP_LeftNavMenuID=%7Bmenuid%3A%27CR_ERP_MyselfParticulars%27%2Cname%3A%27%u6211%u7684%u4FE1%u606F%27%7D; CR_ERP_MyselfParticulars=%7Bmenuid%3A%27AttendanceBook%27%2Cname%3A%27%u6211%u7684%u8003%u52E4%27%7D; testcookie=yes; PHPSESSID=de401e8b753b3fc84b6c5c21b00864c2",
        "Host":"192.168.43.2",
        "Origin":"http://192.168.43.2",
        "Referer":"http://192.168.43.2/erp/index.php",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }

    responseRes = huihuSession.post(postUrl, data = postData, headers = header)
    s = responseRes.content.decode("utf-8")
    #print(s)
    poststart = s.find("name:\'")
    postend = s.find("\',identity:")
    content = s[(poststart + len("name:\'")):postend]
    print(content)

def getinfo():
    getUrl = "http://192.168.43.2/erp/php/attendancefs.php?action=GetAttendanceBookByAttendanceID&appointmentdate=2015-06-08&attendanceid=444190&startdate=2019-08-25&enddate=2019-09-24&time=Mon%20Sep%2030%202019%2009:37:09%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"

    header = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Cookie":"testcookie=yes; employee=%7B%22logintype%22%3A%22email%22%2C%22loginid%22%3A%22wangzhi@crearo.com%22%2C%22department%22%3A%2218%22%2C%22name%22%3A%22%u738B%u7949%22%2C%22identity%22%3A%22wangzhi@crearo.com%22%2C%22departments%22%3A%2218%22%2C%22attendanceid%22%3A%22444190%22%2C%22hexpassword%22%3A%22c639a0e6d07450815dc0938230a197a4%22%2C%22navmenus%22%3A%5B%7B%22menuid%22%3A%22CR_ERP_Employee%22%2C%22name%22%3A%22%u5458%u5DE5%u7BA1%u7406%22%7D%5D%2C%22status%22%3Atrue%7D; CR_ERP_NavMenuID=CR_ERP_Employee; CR_ERP_LeftNavMenuID=%7Bmenuid%3A%27CR_ERP_MyselfParticulars%27%2Cname%3A%27%u6211%u7684%u4FE1%u606F%27%7D; CR_ERP_MyselfParticulars=%7Bmenuid%3A%27AttendanceBook%27%2Cname%3A%27%u6211%u7684%u8003%u52E4%27%7D; PHPSESSID=de401e8b753b3fc84b6c5c21b00864c2",
        "Host":"192.168.43.2",
        "Referer":"http://192.168.43.2/erp/index.php",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }
    
    responseRes = huihuSession.get(getUrl, headers = header, allow_redirects = False)
    s = responseRes.content.decode("utf-8")
    #print(s)
    start = 0
    while 1:
        poststart = s.find("Date:\'", start)
        if (poststart == -1):
            break
        postend = s.find("\',WorkShiftName", poststart + len("Date:\'"))
        content = s[(poststart + len("Date:\'")):postend]

        infostart = s.find("PunchedRecords:\'", poststart)
        if (infostart != -1):
            infoend = s.find("\'},", infostart + len("PunchedRecords:\'"))
            info = s[(infostart + len("PunchedRecords:\'")):infoend]
            if (info != ''):
                print("%s:%s" % (content, info))
            else:
                print("%s: null" % content)

        start = poststart + len("Date:\'")

if __name__ == '__main__':
    #登录ERP
    login()

    #查询打卡记录
    getinfo()
