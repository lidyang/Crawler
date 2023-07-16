import requests,json,os,time
import smtplib
import datetime
import urllib

from email.mime.text import MIMEText
from email.header import Header

import ddddocr


headers={

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers"
}
cookies = {}

def save_img():
    result = {}

    d=int(round(time.time()*1000))
    img_url = 'https://lqcx.haut.edu.cn/zsgk/getGklqcxYzm.do?d='+str(d)
    # print(img_url)

    req = requests.get(url=img_url,headers=headers,allow_redirects=False)
    print("first time： " + str(req.status_code)  + "  "  + str(req.headers))

    if req.status_code !=302:
        return result
    
    cookies = req.cookies
    req = requests.get(url=img_url,headers=headers)
    print("second time： " + str(req.status_code)  + "  "   + str(req.headers))

    if req.status_code !=200:
        return result

    text = req.text
    start = text.index("'cookie' : ")
    end = text.index(",\n                \'uri\'")
    # print(start)
    # print(end)
    substr=text[start:end]
    str_list= substr.split('"')
    if len(str_list) >= 2:
            muyun_sign_javascript=str_list[1]
            # print(muyun_sign_javascript)
            cookies["muyun_sign_javascript"]=muyun_sign_javascript

    # print(cookies)
    req = requests.get(url=img_url,headers=headers,cookies=cookies)
    print("third time： " + str(req.status_code)  + "  "   + str(req.headers))
    if req.status_code !=200:
        return result

    cookies["JSESSIONID"]=req.cookies["JSESSIONID"]

    print("cookies:  "+ str(cookies))

    # print(req.text)
    open(f'temp.jpg','wb').write(req.content)

    result_url = 'https://lqcx.haut.edu.cn/zsgk/getGklqcxJg.do'
    now = datetime.datetime.now()
    code = get_ver_code()
    print(now)

    params={
        "s_ksh": "23411701151030",
        "s_sfzh": "411303200410020530",
        "s_yzm": code
    
    }
    # print(cookies)
    req = requests.post(url=result_url,headers=headers,params=params,cookies=cookies)
    print("last time： " + str(req.status_code)  + "  "   + str(req.headers))
    if req.status_code !=200:
        return result

    print(json.loads(req.text))
    result = json.loads(req.text)
    return result
    

def send_mail(content):
    sm=smtplib.SMTP_SSL('smtp.163.com',port=465)
    aa=sm.login('lidgyang@163.com','OGMHSCLBSGQIEMZS')
    print(aa)
    msg = MIMEText(content,"plain","utf-8")
    msg['Subject'] = Header('高考录取查询')
    sm.sendmail('lidgyang@163.com','1225497135@qq.com',msg.as_string())
    sm.quit()

def get_ver_code():
    ocr = ddddocr.DdddOcr()
    with open('temp.jpg', 'rb') as f:
        image_bytes = f.read()
    res = ocr.classification(image_bytes)
    print(res)
    return res

if __name__ == '__main__':
    while True:
        result = save_img()
        success = str(result.get("success"))
        if success:
            print(success)
            if success=="False":
                print("False")
                print(datetime.datetime.now())
                hour = time.strftime("%H")
                if hour == '17' or hour =='10':
                    send_mail(str(result))
            else:
                print("no")
        else:
            send_mail("获取失败，请检查")

        print("暂停3600秒后继续。。。")
        print(datetime.datetime.now())
        time.sleep(3600) 