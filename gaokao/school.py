# -*- coding=utf-8 -*-

import requests,json,os,time

import smtplib
import pymysql
import datetime

import time
import random


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'accept': 'application/json, text/plain, */*'
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






def get_school_list():
    for i in range(100):
        print("下载第"+str(i+1) + "页")
        url = 'https://api.eol.cn/web/api/?admissions=&central=&department=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&page='+str(i+1)+'&province_id=&school_type=&size=30&type=&uri=apidata/api/gkv3/school/lists&signsafe=44118d38472223581e07be311b6b029b'
        print(url)
        now = datetime.datetime.now()
        print(now)
        list_req = requests.get(url=url,headers=headers)
        # print(list_req.text)

        url_lists_dict = json.loads(list_req.text)
        school_list = url_lists_dict["data"]["item"]
        # print(school_list)

        conn = pymysql.connect(**config)
        print("插入数据---------连接数据库成功")
        cursor = conn.cursor()


        if school_list:
            index=1
            for item in school_list:
                print("================下载第"+str(i*30+index) + "个")
                index = index + 1
                school_dic = {}
                school_dic["school_id"] = item.get("school_id")
                school_dic["name"] = item.get("name")
                school_dic["province_name"] = item.get("province_name")
                school_dic["city_name"] = item.get("city_name")
                school_dic["f211"] = item.get("f211")
                school_dic["f985"] = item.get("f985")
                school_dic["nature_name"] = item.get("nature_name")
                school_dic["type_name"] = item.get("type_name")
                school_dic["level_name"] = item.get("level_name")
                school_dic["province_id"] = item.get("province_id")
                school_dic["dual_class_name"] = item.get("dual_class_name")

                print(school_dic)
                sql = ' INSERT INTO own_db.school (school_id, name, city_name, type_name, level_name, province_id, province_name, f211, f985, nature_name, dual_class_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                value=[item.get('school_id'),item.get('name'),item.get('city_name'),item.get('type_name'),item.get('level_name'),item.get('province_id'),item.get('province_name'),item.get('f211'),item.get('f985'),item.get('nature_name'),item.get('dual_class_name')]
                print(value)
                cursor.execute(sql,value)
                conn.commit()
                print("插入数据："+item.get('name')+"     成功")

        conn.close()
        print("插入数据---------关闭数据库成功")

        
        t=random.randint(5,20)
        print("暂停"+str(t)+"秒后继续。。。")
        print(datetime.datetime.now())


def get_score_detail(id):
    years= [2022,2021,2020,2019,2018]
        
    print("下载学校： "+str(id) + "        的数据")

    conn = pymysql.connect(**config)
    print("插入数据---------连接数据库成功")
    cursor = conn.cursor()
    for year in years:
        url = 'https://static-data.gaokao.cn/www/2.0/schoolprovincescore/'+  str(id)  +'/'+ str(year) + '/41.json'
        print(url)

        resp = requests.get(url=url,headers=headers)

        if resp.status_code == 200:
            print(resp.text)
            print("get school score detail")

            detail_dict=json.loads(resp.text)
            code = detail_dict["code"]
            dic={}
            if code == "0000":
                data = detail_dict.get("data")
                like_data = data.get("1")
                if like_data:
                    num_found = like_data.get("numFound")
                    if num_found >= 1:
                        items = like_data.get("item")
                        for item in items:
                            school_score = {}
                            school_score["school_id"] = item.get("school_id")
                            school_score["local_batch_name"] = item.get("local_batch_name")     #
                            school_score["min"] = item.get("min")                               #最低分
                            school_score["min_section"] = item.get("min_section")               #最低位次
                            school_score["proscore"] = item.get("proscore")                     #省控线
                            school_score["type"] = item.get("type")                             #文理科 理科-1 文科-2
                            school_score["zslx_name"] = item.get("zslx_name")                   #招生类型     
                            school_score["zslx_rank"] = item.get("zslx_rank")
                            school_score["year"] = item.get("year")    

                            print(school_score)

                            sql = ' INSERT INTO own_db.school_score (school_id, local_batch_name, min, min_section, proscore, type, zslx_name, zslx_rank, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                            value=[item.get('school_id'),item.get('local_batch_name'),item.get('min'),item.get('min_section'),item.get('proscore'),item.get('type'),item.get('zslx_name'),item.get('zslx_rank'),item.get('year')]
                            print(value)
                            cursor.execute(sql,value)
                            conn.commit()
                            print("+++++++插入数据："+item.get('school_id')+"，时间： " + str(item.get("year") ) + "     成功!!!")
                            t=random.randint(1,3)
                            print("************暂停"+str(t)+"秒后继续。。。")
                            time.sleep(t)   

    print("插入数据："+str(id)+"     成功")
    conn.close()
    print("插入数据---------关闭数据库成功")



def get_plan(id):

    years= [2023]
        
    print("下载学校： "+str(id) + "        招生计划的数据")

    conn = pymysql.connect(**config)
    print("插入数据---------连接数据库成功")
    cursor = conn.cursor()
    for year in years:
        url = 'https://static-data.gaokao.cn/www/2.0/schoolspecialplan/'+  str(id)  +'/'+ str(year) + '/41.json'
        print(url)
        resp = requests.get(url=url,headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            print("get school plan detail")

            detail_dict=json.loads(resp.text)
            code = detail_dict["code"]
            dic={}
            if code == "0000":
                data = detail_dict.get("data")
                like_data = data.get("1_7_0")
                if like_data:
                    num_found = like_data.get("numFound")
                    if num_found >= 1:
                        items = like_data.get("item")
                        for item in items:
                            school_spe_plan = {}
                            school_spe_plan["school_id"] = item.get("school_id")
                            school_spe_plan["local_batch_name"] = item.get("local_batch_name")     #
                            school_spe_plan["length"] = item.get("length")                               #最低分
                            school_spe_plan["level1_name"] = item.get("level1_name")               #最低位次
                            school_spe_plan["level2_name"] = item.get("level2_name")                     #省控线
                            school_spe_plan["level3_name"] = item.get("level3_name")                             #文理科 理科-1 文科-2
                            school_spe_plan["num"] = item.get("num")                   #招生名额    
                            school_spe_plan["tuition"] = item.get("tuition")    # 学费
                            school_spe_plan["spname"] = item.get("spname")      #专业描述
                            school_spe_plan["spcode"] = item.get("spcode")     #专业代码
                            school_spe_plan["zslx_name"] = item.get("zslx_name")     

                            print(school_spe_plan)
                            sql = ' INSERT INTO own_db.school_plan (school_id, local_batch_name, length, level1_name, level2_name, level3_name, num, tuition, spname, spcode, zslx_name, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                            value=[item.get('school_id'),item.get('local_batch_name'),item.get('length'),item.get('level1_name'),item.get('level2_name'),item.get('level3_name'),item.get('num'),item.get('tuition'),item.get('spname'),item.get("spcode"),item.get("zslx_name"),str(year)]
                            print(value)
                            cursor.execute(sql,value)
                            conn.commit()

            print("+++++++插入招生计划数据："+str(id)+"，时间： " + str(year) + "     成功!!!")

            t=random.randint(1,4)
            print("************暂停"+str(t)+"秒后继续。。。")
            time.sleep(t)   

    print("插入数据："+str(id)+"     成功")
    conn.close()
    print("插入数据---------关闭数据库成功")





def get_plan_score(id):
    # https://static-data.gaokao.cn/www/2.0/schoolspecialscore/391/2020/41.json
    years= [2022,2021,2020,2019,2018]       
    print("下载学校： "+str(id) + "        专业分数的数据")
    conn = pymysql.connect(**config)
    print("插入数据---------连接数据库成功")
    cursor = conn.cursor()
    for year in years:
        url = 'https://static-data.gaokao.cn/www/2.0/schoolspecialscore/'+  str(id)  +'/'+ str(year) + '/41.json'
        print(url)
        resp = requests.get(url=url,headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            print("get school special score detail")

            detail_dict=json.loads(resp.text)
            code = detail_dict["code"]
            dic={}
            if code == "0000":
                data = detail_dict.get("data")
                like_data = data.get("1_7_0")
                if like_data:
                    num_found = like_data.get("numFound")
                    if num_found >= 1:
                        items = like_data.get("item")
                        for item in items:
                            school_spe_score = {}
                            school_spe_score["school_id"] = item.get("school_id")
                            school_spe_score["local_batch_name"] = item.get("local_batch_name")     #
                            school_spe_score["level1_name"] = item.get("level1_name")               #最低位次
                            school_spe_score["level2_name"] = item.get("level2_name")                     #省控线
                            school_spe_score["level3_name"] = item.get("level3_name")  
                            
                            school_spe_score["min"] = item.get("min")                               #最低分
                            school_spe_score["min_section"] = item.get("min_section")               #最低位次
                            school_spe_score["max"] = item.get("max")                     #省控线
                            school_spe_score["zslx_name"] = item.get("zslx_name")                   #招生类型       
                            school_spe_score["spname"] = item.get("spname")      #专业描述

       

                            print(school_spe_score)
                            sql = ' INSERT INTO own_db.school_spe_score (school_id, local_batch_name, level1_name, level2_name, level3_name, min, max, spname, min_section, zslx_name, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                            value=[item.get('school_id'),item.get('local_batch_name'),item.get('level1_name'),item.get('level2_name'),item.get('level3_name'),item.get('min'),item.get('max'),item.get('spname'),item.get("min_section"),item.get("zslx_name"),str(year)]
                            print(value)
                            cursor.execute(sql,value)
                            conn.commit()

            print("+++++++插入招生计划数据："+str(id)+"，时间： " + str(year) + "     成功!!!")

            t=random.randint(1,5)
            print("************暂停"+str(t)+"秒后继续。。。")
            time.sleep(t)   

    print("插入数据："+str(id)+"     成功")
    conn.close()
    print("插入数据---------关闭数据库成功")



def get_school_ids(offset,nums):
    conn = pymysql.connect(**config)
    print("查询学校数据---------连接数据库成功")
    cursor = conn.cursor()
    sql = "select school_id from own_db.school limit " + str(offset) +' , ' + str(nums)
    print(sql)
    result  = cursor.execute(sql)
    # print(result)
 
    rows = cursor.fetchall()
    print(rows)

    print("查询学校数据---------关闭数据库成功")
    ids = []

    if result < 1:
        return ids

    for row in rows:
        # ids.append(row.get("school_id"))
        school_id = row.get("school_id")
        sql2 = "select level_name from own_db.school where school_id =  " + str(school_id)
        # print(sql2)
        result2  = cursor.execute(sql2)
        # print(result2)
        rows2 = cursor.fetchone()
        if rows2.get("level_name") == "普通本科":
            # print(str(id) + ":  " + rows2.get("level_name"))
            ids.append(school_id)
        

    print(ids)
    conn.close()
    return ids



if __name__ == '__main__':

    # start= 228



    # for i in range(60):
    #     print("&&&&&&&&&&&开始下载第：  " + str(i) + "页")
    #     offset =  start + i*50
    #     if offset >2900:
    #         break

    #     rows = 50
    #     ids = get_school_ids(offset,rows)
    #     if ids:
    #         for id in ids:
    #             get_plan(id)
    #             # get_plan_score(id)
    #             # print(1)
                               

    #     print("&&&&&&&&&&&下载第：  " + str(i) + "页成功")          
    #     t=random.randint(3,5)
    #     print("************暂停"+str(t)+"秒后继续。。。")
    #     time.sleep(t)   

    ids = get_school_ids(0,228)
    if ids:
        for id in ids:
            get_plan(id)
            # get_plan_score(id)
            # print(1)
            # a=1



        



