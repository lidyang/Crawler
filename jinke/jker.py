import requests,json,os,time

def get_response(url):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'accept': 'application/x.api.v1+json',
        'cookie': '_ga=GA1.1.1721798892.1646617092; _ga_VQVDVRFE9Z=GS1.1.1653283340.5.1.1653287230.51',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9jY2JmaW50ZWNoLmppa2VyLmNvbVwvd3NcL2FwaVwvbWVtYmVyXC9vYXV0aFwvc2lnbmluXC9qeGprIiwiaWF0IjoxNjUzMjcyNzE0LCJuYmYiOjE2NTMyNzI3MTQsImp0aSI6Ik5FVktlZGhzODlOQTEzaW0iLCJzdWIiOjE5NiwicHJ2IjoiMTQxNDM2MTkwOTcyYjQxNjMzMDY3YjFkZTVmYWU5Y2NmNzE2NTMxYSJ9.w4DtRjXSCUJUOka4UZTpZcWbtDWJkGaN_nctCQdaaTI'
    }
    response = requests.get(url=url,headers=headers)
    return response

def download_vedio(url,filePath,fileName):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'accept': 'application/x.api.v1+json'
        }
    response = requests.get(url=url,headers=headers)
    content = response.content
    tempfilename = filePath+fileName
    with open(tempfilename + ".mp4", "wb") as f:
        f.write(content)

def download_course(url):
    # url = "https://ccbfintech.jiker.com/api/one-course/course/20afd4e8"
    resp = get_response(url=url)

    resp_code=json.loads(resp.text).get('code')
    print("返回状态码：" + str(resp_code))
    if resp_code == 200 :
        contents=json.loads(resp.text).get('data').get('content')
        courseName=json.loads(resp.text).get('data').get('name')
        courseName = courseName.replace('/','-').replace('\\','-').replace(':','：').replace('?','').replace('"','“')
        ch_num = len(contents)

        print("课程： " + courseName + " 共有 " + str(ch_num) + "章")
        for i in range(ch_num):
            print("*****第" + str(i+1) + "章")
            content = contents[i]
            childrens = content.get('children')
            children_num = len(childrens)
            for j in range(children_num): 
                vedio_url = childrens[j].get('url')
                if vedio_url is None:
                    continue
                filePath = 'E:\\work\\jkvedio\\'+courseName+'\\'
                if not os.path.exists(filePath):
                    os.mkdir(filePath)
                
                fileName=str(i+1) + '-' + str(j+1) + '-' + content.get('name') + '-' + childrens[j].get('name')
                fileName = fileName.replace('/','-').replace('\\','-').replace(':','：').replace('?','').replace('"','“')
                print("=====开始下载第" + str(j+1) + "节:  " +  fileName) 
                download_vedio(url=vedio_url,filePath=filePath,fileName=fileName)
                print("=====下载完毕")

        print("课程： " + courseName + " 下载完毕")       
    
    else :
        print("请求错误")
        print(resp.text)
        return


if __name__ == '__main__':

    # 数据科学：基于Python和R语言实现
    # url = "https://ccbfintech.jiker.com/api/one-course/course/b1aa87ec"
    ids = ['b574dee3','12891a30','9c47f710','21aafe14','cb77b8ca','d4735129','f28a9ca3','7d14e952','7cbf442d','e39d8e39','d96705a0']
    for id in ids:
        url = 'https://ccbfintech.jiker.com/api/one-course/course/'+id
        download_course(url)
        print('3秒后开始下载下一个课程')
        time.sleep(3)





    


    #23讲掌握网络安全与渗透 98cc0d94
    # Zabbix从入门到进阶  2fbb8fe5
    # NLP 算法与实践 f0c27dbe
    # 优化Sketch基础篇  c601306a
    # Sketch 进阶与技巧  14ce4fca
    # 手把手教你做产品 c154b04d
    # 从零开始学习产品原型技术 08f1605f
    # Axure 从入门到精通  3d037603
    #  Adobe illustrator软件入门到精通 b574dee3
    # Web安全  12891a30
    #企业渗透测试和持续监控 9c47f710
    # Docker容器入门篇 21aafe14
    # Python RESTful API 开发  cb77b8ca
    # 运维高手的36项修炼  d4735129
    #  数据分析思维  f28a9ca3
    # 敏捷项目管理  9cecf76c
    # Vue.js 前端应用开发  7d14e952
    # Vue.js 前端框架详解  7cbf442d
    # Vue.js 3.0 核心源码解析 e39d8e39
    # 共享单车项目-SPA架构后台管理实战  d96705a0  












