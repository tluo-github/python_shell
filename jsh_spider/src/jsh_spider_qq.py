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
db_help = DbHelp()
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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


def analysis_detail_plus(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    try:
        property_introduce = soup.find(id="housedetailmore").text
    except:
        property_introduce = soup.find(id="housedetailless").text

    property = soup.find(id="property")
    property_parking_space = u"无数据"
    for li in property.find_all("li"):
        key = li.find("span").text
        value = li.find("p").text
        if key == "停车位":
            property_parking_space = value

    dict = {}
    dict['property_introduce'] = property_introduce
    dict['property_parking_space'] = property_parking_space
    return dict

def analysis_detail(html_doc,dict,url):
    soup = BeautifulSoup(html_doc, "html.parser")
    for p in soup.find("div", attrs={'class':'contBorder c9'}).find_all("p"):
        spans = p.find_all("span")
        key = spans[0].text
        value = spans[1].text
        if key == "开盘时间":
            property_opentime = value
        elif key == "入住时间":
            property_deliverytime = value
        elif key == "物业类别":
            property_type = value
        elif key == "产权年限":
            property_chuanquaninanxian = value
        elif key == "装修情况":
            property_zhuangxiu = value
        elif key == "建筑类别":
            property_jianzhu_type = value
        elif key == "总户数":
            property_households_number = value
        elif key == "占地面积":
            property_zhandimianji = value
        elif key == "建筑面积":
            property_jianzhummianji = value
        elif key == "绿化率":
            property_greening_rate = value
        elif key == "容积率":
            property_volume_rate = value
        elif key == "开发商":
            property_developers = value
        elif key == "预售证":
            property_yushouzheng = value
        elif key == "物业公司":
            property_costs = value

    dict['property_opentime'] = property_opentime
    dict['property_deliverytime'] = property_deliverytime
    dict['property_type'] = property_type
    dict['property_chuanquaninanxian'] = property_chuanquaninanxian
    dict['property_zhuangxiu'] = property_zhuangxiu
    dict['property_jianzhu_type'] = property_jianzhu_type
    dict['property_households_number'] = property_households_number
    dict['property_zhandimianji'] = property_zhandimianji
    dict['property_jianzhummianji'] = property_jianzhummianji
    dict['property_greening_rate'] = property_greening_rate
    dict['property_volume_rate'] = property_volume_rate
    dict['property_developers'] = property_developers
    dict['property_yushouzheng'] = property_yushouzheng
    dict['property_costs'] = property_costs

    url = url.replace('m.', '') + "info.shtml"
    html_doc = init_selenium(url=url)
    dict_plus = analysis_detail_plus(html_doc)
    dict['property_introduce'] = dict_plus['property_introduce']
    dict['property_parking_space'] = dict_plus['property_parking_space']
    db_help.insert_forqq(dict)

def analysis(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    newHouseList = soup.find(id="newHouseList")
    for item in newHouseList.find_all("div",attrs={'class':'item'}):
        sleep(random.uniform(0.5, 1))  # 睡眠函数用于防止爬取过快被封IP
        dict = {}
        property_name = item.find("h3").text
        property_image = item.find("img").get("src")
        property_area = item.find("div", attrs={'class': 'left'}).text
        arr = []
        for em in item.find("p", attrs={'class': 'feature'}).find_all("span"):
            arr.append(em.text)
        property_label = ','.join(arr)

        arr = []
        for em in item.find("div", attrs={'class': 'right'}).find_all("span"):
            arr.append(em.text)
        property_price = ''.join(arr)
        property_address = item.find("div", attrs={'class': 'intro'}).find("p").text
        dict['property_name'] = property_name
        dict['property_image'] = property_image
        dict['property_area'] = property_area
        dict['property_label'] = property_label
        dict['property_price'] = property_price
        dict['property_address'] = property_address
        url = item.find('a').get('href')
        print("[*] begin get url:" + url)
        r = requests.get(url=url, headers=app_headers)
        if r.status_code == 200:
            analysis_detail(html_doc=r.text, dict=dict, url=url)
            #exit(0)
        else:
            print "[-]Error:get fail for: " + url

def init_selenium(url):
    print("[*] begin get url：" + url)
    driver.get(url)
    assert "腾讯房产" in driver.title
    html_doc = driver.page_source
    return html_doc

chromedriver = "F:\software\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

def main():
    global  driver
    driver.get("http://m.db.house.qq.com/search/jingzhou/")
    assert "腾讯房产" in driver.title
    for index in range(0,7):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    ele = driver.find_element_by_id('loadingpic')
    time.sleep(1)
    html_doc = driver.page_source
    analysis(html_doc=html_doc)

def test():
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <div class="item">
    <a bosszone="boss3355,newhouse" href="http://m.db.house.qq.com/jingzhou_178339/">
    <div class="li-item">
    <div class="img">
    <p class="pr">
    <img src="http://p1.qpic.cn/estate/0/3655a3c1e1fd1a95a2c971842c78fad9.jpg/135"/>
    </p>
    </div>
    <div class="intro">
    <h3>恒大金名都</h3>
    <div>
    <div class="left">荆北新区</div>
    <div class="right">
    <span class="youhui">待定</span><span></span>
    </div>
    </div>
    <p>荆州火车站站前广场正前300米</p>
    <p class="feature">
    <span>品牌开发商</span><span>生态宜居</span> </p>
    </div>
    </div>
    </a>
    </div>
    </body>
    """
    soup = BeautifulSoup(html_doc, "html.parser")
    item = soup.find("div", attrs={'class': 'item'})
    dict = {}
    property_name = item.find("h3").text
    property_image = item.find("img").get("src")
    property_area = item.find("div", attrs={'class':'left'}).text
    arr = []
    for em in item.find("p", attrs={'class': 'feature'}).find_all("span"):
        arr.append(em.text)
    property_label = ','.join(arr)

    arr = []
    for em in item.find("div", attrs={'class': 'right'}).find_all("span"):
        arr.append(em.text)
    property_price = ''.join(arr)
    property_address = item.find("div", attrs={'class': 'intro'}).find("p").text
    dict['property_name'] = property_name
    dict['property_image'] = property_image
    dict['property_area'] = property_area
    dict['property_label'] = property_label
    dict['property_price'] = property_price
    dict['property_address'] = property_address
    url = item.find('a').get('href')
    print("[*] begin get url:" + url)
    r = requests.get(url=url, headers=app_headers)
    if r.status_code == 200:
        analysis_detail(html_doc=r.text, dict=dict, url=url)
        # exit(0)
    else:
        print "[-]Error:get fail for: " + url



if __name__ == "__main__":
    main()

