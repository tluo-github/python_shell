#!/usr/bin/python
#coding:utf-8
'''
功能：荆房网 新房数据爬取
日期: 2016-12-19
版本: V1
'''
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
from DbHelp import DbHelp


__author__ = 'Bruce'

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
db_help = DbHelp()

def analysis_detail(html_doc,title):
    dict = {}
    dict['property_name'] = title
    soup = BeautifulSoup(html_doc, "html.parser")
    loupan_info = soup.find("div", attrs={"class": "box box_up"})
    try:
        loupan_image = soup.find("div", attrs={"class": "act_top_show"}).find("img")
        property_image = str(loupan_image.get("src"))
        dict['property_image'] = property_image
    except:
        dict['property_image'] = u"无数据"

    try:
        property_introduce = soup.find_all("div", attrs={"class": "box_info"})[1].text
    except:
        property_introduce = soup.find_all("div", attrs={"class": "box_info"})[0].text
    dict['property_introduce']= property_introduce

    for li in loupan_info.find("ul").find("ul").find_all_next("li"):
        #print(li.text)
        arr = li.text.encode("utf-8").split('：')
        if arr[0] == "售楼处电话" :
            dict['property_tel'] =  unicode(arr[1], "utf-8")
        elif arr[0] == "开发商":
            dict['property_developers'] = unicode(arr[1], "utf-8")
        elif arr[0] == "楼盘地址":
            dict['property_address'] = unicode(arr[1], "utf-8")
        elif arr[0] == "销售均价":
            dict['property_price'] = unicode(arr[1], "utf-8")
        elif arr[0] == "售楼处地址":
            dict['property_salesoffices'] = unicode(arr[1], "utf-8")
        elif arr[0] == "容积率":
            dict['property_volume_rate'] =  unicode(arr[1], "utf-8")
        elif arr[0] == "绿化率":
            dict['property_greening_rate'] =  unicode(arr[1], "utf-8")
        elif arr[0] == "住宅物业费":
            dict['property_costs'] =  unicode(arr[1], "utf-8")
        elif arr[0] == "车位数":
            dict['property_parking_space'] =  unicode(arr[1], "utf-8")
        elif arr[0] == "规划户数":
            dict['property_households_number'] =  unicode(arr[1], "utf-8")
        elif arr[0] == "物业类型":
            dict['property_type'] = unicode(arr[1], "utf-8")
        elif arr[0] == "入住时间":
            if arr[1] == "":
                dict['property_deliverytime'] = u'无数据'
            else:
                dict['property_deliverytime'] =  unicode(arr[1], "utf-8")

    db_help.insertJsh(dict)
def analysis(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    #print soup.title.string
    for link in soup.find(id="list").find_all("a"):
        print ("\t" + link.find("span").text + ": " + link.get('href'))
        r = requests.get(url=link.get('href'), headers=headers)
        if r.status_code == 200:
            analysis_detail(html_doc=r.text, title=link.find("span").text)
            #exit(0)
        else:
            print "[-]Error:get fail for: " + link.get('href')

def main():
    for index in range(1, 17):
        sleep(random.uniform(0.5, 1))  # 睡眠函数用于防止爬取过快被封IP
        url = "http://wap.0716fw.com/loupan/" + str(index)
        print ("[*] begin start get : " + url)
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            analysis(html_doc=r.text)
        else:
            print "[-]Error:get fail for: " + url
            break
if __name__ == "__main__":
    main()