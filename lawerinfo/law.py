import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import random

cookie_list = {}

def main():
   
    for j in range(0,148):
        downContent(j)

   

    print("END")

def downContent(j):

     # 1. 指定url
    url = "https://law.sysu.edu.cn/library/books?page="+str(j)

    # 2. UA伪装
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "max-age=0",
        'Connection': "keep-alive",
        'Host': "law.sysu.edu.cn",
        'Sec-Fetch-Dest': "document",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-Site': "none",
        'Sec-Fetch-User': "?1",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0  Safari/537.36"
    }

    cookie_dic = get_cookie()

    # print(cookie_dic)
    cookie = 'SESS5089e3a76df5f75b023fd0b6c7bfa470=IQaZVWA5DxER1Fya_CHe-9xYiqNY9Yq8BadO53zXAgM; ZMRhjlxmTSDe443S='+ cookie_dic["ZMRhjlxmTSDe443S"] +'; ZMRhjlxmTSDe443T='+ cookie_dic["ZMRhjlxmTSDe443T"]+'; has_js=1'
    # cookie = 'ZMRhjlxmTSDe443S=TVGRM7EGBS_VFageikUuvp7pEJ6U5rtrJnfOfDe3VPyJWg8BY2qL9I1kyTAPu5Ne; has_js=1; ZMRhjlxmTSDe443T=5tJlx22Ov.KJVPL9tWXc3eE9l9hyVxXG.tF7RsR60T_prRS3hSGzl0.2iDyvK8Exnrfqob8oxdwVDmXmTdsicuZFSgMWJMoCgfQmRyOChcHQDKUsZZPeorpEgJAbzFbIN6tcNOngLALyJuRrTF11Yjjy1DdSrRLtgdN9U0F7LNn7bD3N.70CJFA7TndNXHk5TnXx3kl6eFTDhj_wo5nGbXO2x41_RCRW3IPeB7E8aHb2w.aKdc3AdqkeBsqauQ6ACSt3y1iVRcm6tit3kjtiMHVwlhFczPr03iR02tWmOXyGp.NVrSJqTfx3nngjtTWHykj21NcUC4G8NwVrYu.CegTa6'
    # print(cookie)
    headers['Cookie']=cookie


    # print(headers)
    # 3. 发起请求
    response = requests.get(url=url, headers=headers)
    # 4. 获取响应数据
    page_text = response.text
    status = response.status_code
    print("status: " + str(status))
    if status != 200:
        return 0
    
    soup=BeautifulSoup(page_text,'html.parser')

    tbody = soup.find_all('tbody')[0]
    res = []
    print(len(tbody.contents))
    i=0
    for child in tbody.children:
       
        # print(child)
        if child.name == 'tr' :
            i=i+1
            book = child.find('td',class_='views-field-field-book-flh').text.strip()
            book = book + '|#|' + child.find('td',class_='views-field-title').text.strip()
            book = book + '|#|' + child.find('td',class_='views-field-field-book-author').text.strip()
            book = book + '|#|' + child.find('td',class_='views-field-field-book-cbs').text.strip()            
            book = book + '|#|' + child.find('td',class_='views-field-field-book-rq').text.strip()
            book = book + '|#|' + child.find('td',class_='views-field-field-book-isbn').text.strip()            
            book = book + '|#|' + child.find('td',class_='views-field-field-field-book-zt2').text.strip()+'\n'                      
            # print(book)
            res.append(book)

        # else :
            # print('child is null')

    print(i)
    res_str = "第"+ str(j) +"次下载，共下载" + str(i) +"页;"
    print(res_str)
    # print(res)
    # 5. 持久化存储
    with open("ans1.csv", "a", encoding="utf-8") as f:
        f.writelines(res)

        t=random.randint(10,20)
        
    print("暂停"+str(t)+"秒后继续。。。")

    time.sleep(t)




def is_valid_of_cookie():
    if not cookie_list:
        return False
    for cookie in cookie_list:
        if cookie.has_key('name') and cookie.has_key('value') and cookie.has_key('expiry'):
            expiry_date = int(cookie['expiry'])
            if expiry_date < int( time.time()):
                return False
    
    return True


def get_cookie():
    cookie_dic={}
    # if not is_valid_of_cookie():
        # driver = webdriver.Chrome()
        # driver.get("https://law.sysu.edu.cn/library/books?page=1")
        # cookie_list = driver.get_cookies()
        # print("cookie_list:")
        # print(cookie_list)

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--headless")
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0  Safari/537.36')

    driver = webdriver.Chrome(options=option)

    with open('stealth.min.js') as f:
        js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
    })

    
    # driver = webdriver.Firefox()
    driver.get("https://law.sysu.edu.cn/library/books?page=1")
    cookie_list = driver.get_cookies()

    # print("cookie_list:")
    # print(cookie_list)
    for cookie in cookie_list:
        cookie_dic[cookie['name']]=cookie['value']
    return cookie_dic

if __name__ == '__main__':
    main()
