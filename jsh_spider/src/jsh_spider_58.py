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
import threading
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
__author__ = 'Bruce'

app_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
           'Cache-Control':'max-age=0',
           'Connection':'keep-alive',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch'}

pc_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99',
           'Cache-Control':'max-age=0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch'}

db_help = DbHelp()

def analysis_detail(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    section = soup.find("section")
    try:
        cheap_room_image = section.find("ul").find("li").find("img").get("data-url")
    except:
        cheap_room_image= u""
    cheap_room_releasetime = section.find("dl", attrs={'class':'name-info'}).find("dd").text.strip()
    for infor_price in section.find("ul",attrs={'class':'infor-price'}).find_all("li"):
        tmp_str = infor_price.text.encode("utf-8")
        if tmp_str.find("面积") == 0:
            cheap_room_acreage = infor_price.find("i").text
        elif tmp_str.find("售价") == 0:
            cheap_room_price = infor_price.find("i").text
        elif tmp_str.find("户型") == 0:
            cheap_room_unit = infor_price.find("i").text
    for room_price in section.find("ul",attrs={'class':'infor-other two-row'}).find_all("li"):
        tmp_str = room_price.text.encode("utf-8")
        if tmp_str.find("单价") == 0:
            cheap_room_unit_price = room_price.find("span").text
        elif tmp_str.find("朝向") == 0:
            cheap_room_towards = room_price.find("i").text
        elif tmp_str.find("楼层") == 0:
            cheap_room_floor = room_price.find("i").text
        elif tmp_str.find("位置") == 0:
            cheap_room_area = room_price.find("i").text
    cheap_room_decade = u"无数据"
    for descrip_infor in section.find("ul",attrs={'class':'descrip-infor two-row mt15'}).find_all("li"):
        tmp_str = descrip_infor.text.encode("utf-8")
        if tmp_str.find("房龄") == 0:
            cheap_room_decade = descrip_infor.find("i").text
        elif tmp_str.find("装修") == 0:
            cheap_room_decoration = descrip_infor.find("i").text

    cheap_room_promulgator = section.find("ul", attrs={'class':'contact'}).find('li',attrs={'class':'black'}).text
    cheap_room_telephone  = section.find("ul", attrs={'class':'contact'}).find('li',attrs={'class':'yellow topPhoneValue'}).text.strip()
    cheap_room_name = section.find(id="titlename").text

    arr = []
    for em in section.find("ul",attrs={'class':'infor-keyword mtlr15'}).find_all("li"):
        arr.append(em.text)
    cheap_room_label = ','.join(arr)
    try:
        cheap_room_cell = soup.find(id="xiaoquName").text
    except:
        cheap_room_cell = "无数据"
    cheap_room_description = section.find(id="descript").find("p").text.strip()
    dict = {}
    dict['cheap_room_name'] = cheap_room_name
    dict['cheap_room_image'] = cheap_room_image
    dict['cheap_room_releasetime'] = cheap_room_releasetime
    dict['cheap_room_price'] = cheap_room_price
    dict['cheap_room_unit'] = cheap_room_unit
    dict['cheap_room_acreage'] = cheap_room_acreage
    dict['cheap_room_label'] = cheap_room_label
    dict['cheap_room_unit_price'] = cheap_room_unit_price
    dict['cheap_room_towards'] = cheap_room_towards
    dict['cheap_room_floor'] = cheap_room_floor
    dict['cheap_room_decoration'] = cheap_room_decoration
    dict['cheap_room_area'] = cheap_room_area
    dict['cheap_room_decade'] = cheap_room_decade
    dict['cheap_room_cell'] = cheap_room_cell
    dict['cheap_room_description'] = cheap_room_description
    dict['cheap_room_promulgator'] = cheap_room_promulgator
    dict['cheap_room_telephone'] = cheap_room_telephone
    db_help.insert_room2(dict=dict)
def get_html_for_url(url):
    r = requests.get(url=url, headers=app_headers)
    if r.status_code == 200:
        analysis_detail(html_doc=r.text)
        #exit(0)
    else:
        print "[-]Error:get fail for: " + url


def analysis(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    ul = soup.find("ul",attrs={'class':'list-info hpic'})
    for li in ul.find_all("li"):
        sleep(random.uniform(0.5, 1))  # 睡眠函数用于防止爬取过快被封IP
        infoid = li.get("infoid")
        #url = "http://m.58.com/jingzhou/ershoufang/25886752262571x.shtml"
        url = "http://m.58.com/jingzhou/ershoufang/"+infoid+"x.shtml"
        #print ("[*] begin start get : " + url)
        try:
            get_html_for_url(url)
        except Exception,e:
            print ("[-] Waring this url faild. begin restart get :" + url)
            print Exception, ":", e

def analysis_v2(url):
    print ("[*] begin start get : " + url)
    try:
        r = requests.get(url=url, headers=pc_headers)
    except:
        r = requests.get(url=url, headers=pc_headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        tbody = soup.find("table", attrs={'class': 'tbimg'})
        for tr in tbody.find_all("tr"):
            a = tr.find("p", attrs={'class': 'bthead'}).find("a", attrs={'class': 't'})
            infoid = a.get("infoid")
            url = "http://m.58.com/jingzhou/ershoufang/" + infoid + "x.shtml"
            print ("[*] url:" + url)
            print ("\t[*] begin start get : " + url)
            try:
                get_html_for_url(url)
            except Exception, e:
                print ("[-] Waring this url faild. begin restart get :" + url)
                print Exception, ":", e
    else:
        print "[-]Error:get fail for: " + url
        exit

def main():
    for index in range(1, 13):
        sleep(random.uniform(0.5, 1))  # 睡眠函数用于防止爬取过快被封IP
        #url = "http://jingzhou.58.com/shashiqu/ershoufang/pn" + str(index)
        #url = "http://jingzhou.58.com/jingjingzhou/ershoufang/pn" + str(index)
        #url = "http://jingzhou.58.com/honghu/ershoufang/pn" + str(index)
        #url = "http://jingzhou.58.com/shishou/ershoufang/pn" + str(index)
        #url = "http://jingzhou.58.com/songzi/ershoufang/pn" + str(index)
        #url = "http://jingzhou.58.com/jianli/ershoufang/pn" + str(index)
        #url = "http://jingzhou.58.com/gongan/ershoufang/pn" + str(index)
        url = "http://jingzhou.58.com/jiangling/ershoufang/pn" + str(index)
        analysis_v2(url=url)
    # url = "http://m.58.com/jingzhou/ershoufang"
    # print ("[*] begin start get : " + url)
    # r = requests.get(url=url, headers=app_headers)
    # if r.status_code == 200:
    #     analysis(html_doc=r.text)
    # else:
    #     print "[-]Error:get fail for: " + url
    #     exit
def test():
    url = "http://m.58.com/jingzhou/ershoufang/25886752262571x.shtml"
    print ("[*] begin start get : " + url)
    r = requests.get(url=url, headers=app_headers)
    if r.status_code == 200:
         print(r.text)
    else:
        print "[-]Error:get fail for: " + url
        exit
if __name__ == "__main__":
    main()