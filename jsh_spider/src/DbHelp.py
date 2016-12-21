#!/usr/bin/python
#coding:utf-8

'''
功能：数据库操作
日期: 2016-12-19
版本: V1
'''
import MySQLdb
#数据库操作
class DbHelp(object):
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = '123456'
        self.db = 'spider'
        self.charset = 'utf8'
        self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)
        self.cursor = self.conn.cursor()


    def insert(self,sql):
        n = self.cursor.execute(sql)
        self.conn.commit()


    def queryAll(self,table):
        sql = "select * from  %s" % table
        n = self.cursor.execute(sql)
        print self.cursor.fetchall()

    def insert_forqq(self, dict):
        insertSQL = "insert into jsh_app_qq (" \
                    "property_name," \
                    "property_image," \
                    "property_area," \
                    "property_label," \
                    "property_price," \
                    "property_address," \
                    "property_opentime," \
                    "property_deliverytime," \
                    "property_type," \
                    "property_chuanquaninanxian," \
                    "property_zhuangxiu," \
                    "property_jianzhu_type," \
                    "property_households_number," \
                    "property_zhandimianji," \
                    "property_jianzhummianji," \
                    "property_greening_rate," \
                    "property_volume_rate," \
                    "property_developers," \
                    "property_yushouzheng," \
                    "property_costs," \
                    "property_introduce," \
                    "property_parking_space) VALUES (" \
                    "'" + dict['property_name'] + \
                    "','" + dict['property_image'] + \
                    "','" + dict['property_area'] + \
                    "','" + dict['property_label'] + \
                    "','" + dict['property_price'] + \
                    "','" + dict['property_address'] + \
                    "','" + dict['property_opentime'] + \
                    "','" + dict['property_deliverytime'] + \
                    "','" + dict['property_type'] + \
                    "','" + dict['property_chuanquaninanxian'] + \
                    "','" + dict['property_zhuangxiu'] + \
                    "','" + dict['property_jianzhu_type'] + \
                    "','" + dict['property_households_number'] + \
                    "','" + dict['property_zhandimianji'] + \
                    "','" + dict['property_jianzhummianji'] + \
                    "','" + dict['property_greening_rate'] + \
                    "','" + dict['property_volume_rate'] + \
                    "','" + dict['property_developers'] + \
                    "','" + dict['property_yushouzheng'] + \
                    "','" + dict['property_costs'] + \
                    "','" + dict['property_introduce'] + \
                    "','" + dict['property_parking_space'] + "')"
        n = self.cursor.execute(insertSQL)
        self.conn.commit()
        print("\t[+] Success:insert mysql ok")
    def insert_room2(self,dict):
        insertSQL = "insert into jsh_app_cheap_room2 (" \
                    "cheap_room_name," \
                    "cheap_room_image," \
                    "cheap_room_releasetime," \
                    "cheap_room_price," \
                    "cheap_room_unit," \
                    "cheap_room_acreage," \
                    "cheap_room_label," \
                    "cheap_room_unit_price," \
                    "cheap_room_towards," \
                    "cheap_room_floor," \
                    "cheap_room_decoration," \
                    "cheap_room_area," \
                    "cheap_room_decade," \
                    "cheap_room_cell," \
                    "cheap_room_description," \
                    "cheap_room_promulgator," \
                    "cheap_room_telephone) VALUES (" \
                    "'"+dict['cheap_room_name']+\
                    "','"+dict['cheap_room_image']+\
                    "','"+dict['cheap_room_releasetime']+\
                    "','"+dict['cheap_room_price']+ \
                    "','" + dict['cheap_room_unit'] + \
                    "','"+dict['cheap_room_acreage']+\
                    "','"+dict['cheap_room_label']+\
                    "','"+dict['cheap_room_unit_price']+\
                    "','"+dict['cheap_room_towards']+\
                    "','"+dict['cheap_room_floor']+\
                    "','"+dict['cheap_room_decoration']+\
                    "','"+dict['cheap_room_area']+\
                    "','"+dict['cheap_room_decade']+ \
                    "','" + dict['cheap_room_cell'] + \
                    "','" + dict['cheap_room_description'] + \
                    "','" + dict['cheap_room_promulgator'] + \
                    "','"+dict['cheap_room_telephone']+"')"
        n = self.cursor.execute(insertSQL)
        self.conn.commit()
        print("\t[+] Success:insert mysql ok")
    def insertJsh(self,dict):
        insertSQL = "insert into jsh_app_test(" \
                    "property_name," \
                    "property_introduce," \
                    "property_image," \
                    "property_tel," \
                    "property_developers," \
                    "property_address," \
                    "property_price," \
                    "property_salesoffices," \
                    "property_volume_rate," \
                    "property_greening_rate," \
                    "property_costs," \
                    "property_parking_space," \
                    "property_households_number," \
                    "property_type," \
                    "property_deliverytime) VALUES (" \
                    "'"+dict['property_name']+\
                    "','"+dict['property_introduce']+\
                    "','"+dict['property_image']+\
                    "','"+dict['property_tel']+ \
                    "','" + dict['property_developers'] + \
                    "','"+dict['property_address']+\
                    "','"+dict['property_price']+\
                    "','"+dict['property_salesoffices']+\
                    "','"+dict['property_volume_rate']+\
                    "','"+dict['property_greening_rate']+\
                    "','"+dict['property_costs']+\
                    "','"+dict['property_parking_space']+\
                    "','"+dict['property_households_number']+ \
                    "','" + dict['property_type'] + \
                    "','"+dict['property_deliverytime']+"')"

        n = self.cursor.execute(insertSQL)
        self.conn.commit()


    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
