import requests,json,os,time

import smtplib
import pymysql
import datetime

import time
import random

from email.mime.text import MIMEText
from email.header import Header


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookie = 'v_v-s-dbsec_vue=6fa8c00d-d302-4cca-8187-f6433773efd3; x-access-token=NdyUbefPYLpTNBoe; userInfo={%22uid%22:3}; sSignature=7751c80c-5d0c-4ada-8205-d150fda00740; menuId=1400502'
token = 'NdyUbefPYLpTNBoe'
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'cookie': cookie,
    'X-Access-Token':token
}

config = {
    'host': '112.74.49.151',
    'port': 3306 ,
    'user': 'root',
    'password': 'root',
    'db': 'own_db',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor

}

def get_db_list(item):
    conn = pymysql.connect(**config)
    print("获取数据--------连接数据库成功")
    cursor = conn.cursor()
    sql = "select * from teacher where name=%s and mail=%s;"
    value=(item.get('name'),item.get('email'))
    cursor.execute(sql,value)
    data = cursor.fetchall()

    print(data)
    print("获取数据成功")

    conn.close()
    cursor.close()
    print("获取数据-------关闭数据库成功")

    return data

def insert_db_item(item):
    conn = pymysql.connect(**config)
    print("插入数据---------连接数据库成功")
    cursor = conn.cursor()
    sql = 'insert into teacher(name, mail, dept, yjfx, mobile) values (%s,%s,%s,%s,%s);'
    value=[item.get('name'),item.get('email'),item.get('dept'),item.get('yjfx'),item.get('mobile')]
    cursor.execute(sql,value)
    conn.commit()
    print("插入数据成功")
    cursor.close()
    conn.close()
    print("插入数据---------关闭数据库成功")



def get_ids():
    url = 'https://10.8.4.200/api/dsms/behaviorRetrieval/getBehaviorList'


    now = datetime.datetime.now()
    # print(now)
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
    print(zeroToday)
    # 获取23:59:59
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    print(lastToday)
    
    params={
        "startTime":str(zeroToday),
        "endTime":str(lastToday),
        "urlTempHost":"",
        "urlParam":"",
        "clientAddr":"",
        "serverAddr":"",
        "appIds":["416004689170501"],
        "reqMethod":"",
        "userTypeName":"",
        "userType":"",
        "dictNames":[],
        "current":"1",
        "pageSize":"200",
        "sortName":"insertTime",
        "sortValue":"descending",
        "isSen":"1",
        "appuserName":"",
        "appDomian":"",
        "apiUrlName":"",
        "apiTypes":[],
        "apitypeAndOr":"0",
        "reqUserAgent":"",
        "reqRefer":"",
        "userAgentType":[],
        "protocolType":"",
        "isInvolve":[],
        "clientPort":"",
        "serverPort":"",
        "clientCountry":"",
        "clientProvince":"",
        "clientCity":"",
        "clientDistrict":"",
        "respContentLength":"",
        "reqBody":"bean.EMAIL",
        "respBody":"",
        "reqContentType":[],
        "respContentType":[],
        "appassetGroupIds":[]
    }
    list_req = requests.post(url=url,headers=headers,json=params,verify=False)

    print(list_req.text)
    url_lists_dict = json.loads(list_req.text)
    # url_lists_dict = list_req.json
    url_lists = url_lists_dict["content"]["list"]
    print(url_lists)
    ids = []
    if not url_lists:
        return ids
    else:
        for item in url_lists:
            id = item["id"]
            print(id)
            ids.append(id)    
        return ids
    

def get_login_ids(second):

    print("get login ids")
    url = 'https://10.8.4.200/api/dsms/behaviorRetrieval/getBehaviorList'
    now = datetime.datetime.now()
    # print(now)
    startime = now - datetime.timedelta(seconds=second,microseconds=now.microsecond)
    print(startime)

    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
    # print(zeroToday)
    # 获取23:59:59
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    print(lastToday)
    
    params={
        "startTime":str(startime),
        "endTime":str(lastToday),
        "urlTempHost":"/review/base/frame/login.do",
        "urlParam":"",
        "clientAddr":"",
        "serverAddr":"",
        "appIds":["416004689170501"],
        "reqMethod":"",
        "userTypeName":"",
        "userType":"",
        "dictNames":[],
        "current":"1",
        "pageSize":"200",
        "sortName":"insertTime",
        "sortValue":"descending",
        "isSen":"1",
        "appuserName":"",
        "appDomian":"",
        "apiUrlName":"",
        "apiTypes":[],
        "apitypeAndOr":"0",
        "reqUserAgent":"",
        "reqRefer":"",
        "userAgentType":[],
        "protocolType":"",
        "isInvolve":[],
        "clientPort":"",
        "serverPort":"",
        "clientCountry":"",
        "clientProvince":"",
        "clientCity":"",
        "clientDistrict":"",
        "respContentLength":"",
        "reqBody":"",
        "respBody":"",
        "reqContentType":[],
        "respContentType":[],
        "appassetGroupIds":[]
    }

    list_req = requests.post(url=url,headers=headers,json=params,verify=False)

    # print(list_req.text)
    url_lists_dict = json.loads(list_req.text)
    # url_lists_dict = list_req.json
    url_lists = url_lists_dict["content"]["list"]
    # print(url_lists)
    ids = []
    if not url_lists:
        return ids
    else:
        for item in url_lists:
            id = item["id"]
            # print(id)
            ids.append(id)   

        print(ids)

        return ids
    


def get_detail(id):
    url = 'https://10.8.4.200/api/dsms/sensitiveDataRetrieval/getDataItemByType'
    params = {
        "id": id
    }
    res = requests.post(url=url,headers=headers,params=params,verify=False)

    # print(res.text)
    detail_dict=json.loads(res.text)
    code = detail_dict["code"]
    dic={}
    if code != 200:
        message = detail_dict["message"]
        dic["status"] = 0
        dic["message"] = message
        return dict

    content = detail_dict["content"]
    req_body = content["reqBody"]

    # print(req_body)
    # req_body = req_body.replace('&lt;span class=&quot;light&quot;&gt;&lt;span class=&quot;light&quot;&gt;','')
    # req_body = req_body.replace('&lt;/span&gt;&lt;/span&gt;','')
    req_body = req_body.replace('&lt;span class=&quot;light&quot;&gt;','')
    req_body = req_body.replace('&lt;/span&gt;','')
    req_body = req_body.replace('epx&2019','')
    strs = req_body.split("&")

    for s in strs:
        # print(s)
        index = s.index("=")
        dic["status"] = 1
        if s[0:index]=="bean.NAME":
            dic["name"] = s[index+1:]
        if s[0:index]=="bean.DEPT":
            dic["dept"] = s[index+1:]
        if s[0:index]=="bean.YJFX":
            dic["yjfx"] = s[index+1:]        
        if s[0:index]=="bean.MOBILE":
            dic["mobile"] = s[index+1:]
        if s[0:index]=="bean.EMAIL":
            dic["email"] = s[index+1:]
   
    # print(dic)

    if dic.get("email") is not None or dic.get("name") is not None:
        db_teacher_list = get_db_list(dic)
        if len(db_teacher_list) == 0 :
            print("数据库无数据，插入新数据")
            insert_db_item(dic)
            content = str(dic)
            send_mail(content)
        else:
            print("该数据数据库已经存在")
        # return dic
    else:
        print("数据为空")
    # print(res.text)



def get_login_detail(id):

    url = 'https://10.8.4.200/api/dsms/sensitiveDataRetrieval/getDataItemByType'
    params = {
        "id": id
    }
    res = requests.post(url=url,headers=headers,params=params,verify=False)

    print("get login detail")

    # print(res.text)
    detail_dict=json.loads(res.text)
    code = detail_dict["code"]
    dic={}
    if code != 200:
        message = detail_dict["message"]
        dic["status"] = 0
        dic["message"] = message
        return dict

    content = detail_dict["content"]
    req_body = content.get("reqBody")
    dic["realAddr"] = content.get("realAddr")
    dic["clientArea"] = content.get("clientArea")
    # dic["reqBody"] = content.get("reqBody")
    dic["insertTime"] = content.get("insertTime")


    print(req_body)
    req_body = req_body.replace('&lt;span class=&quot;light&quot;&gt;','')
    req_body = req_body.replace('&lt;/span&gt;','')
    
      

    strs = req_body.split("&")

    for s in strs:
        print(s)
        index = s.index("=")
        dic["status"] = 1
        if s[0:index]=="CODE":
            dic["CODE"] = s[index+1:]
        if s[0:index]=="EMAIL":
            dic["EMAIL"] = s[index+1:]

    print(dic)

    if dic.get("EMAIL") is not None :
        print("记录登录")
        content = str(dic)
        send_mail(content)
        # return dic
    else:
        print("数据为空")
    # print(res.text)


def send_mail(content):
    sm=smtplib.SMTP()
    sm.connect('smtp.163.com')
    aa=sm.login('lidgyang@163.com','PWQNEZNUYMOUCNJY')
    print(aa)


    msg = MIMEText("新增数据：   " + content,"plain","utf-8")
    msg['Subject'] = Header('python测试')

    sm.sendmail('lidgyang@163.com','65528009@qq.com',msg.as_string())
    sm.sendmail('lidgyang@163.com','1225497135@qq.com',msg.as_string())

    sm.quit()




if __name__ == '__main__':

    t=100
    while True:   
        ids = get_ids()
        for id in ids:
            get_detail(id)

        print("t=" + str(t))
        print(datetime.datetime.now())
        login_ids = get_login_ids(t+10)
        for id in login_ids:
            get_login_detail(id)


        t=random.randint(200,500)
        print("暂停"+str(t)+"秒后继续。。。")
        print(datetime.datetime.now())

        
        time.sleep(t)   




        



