#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         获取Docker 容器静态数据脚本
# Purpose:      获取Docker 容器静态数据(主机名(salt)、操作系统、系统内核、CPU核数、CPU型号、IP地址)
# Version:      2.0 (链接数据库将不重复的插入数据库)
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
import salt.client
import MySQLdb

#该类获得被控机器情况
class Dockerinfo(object):
    def __init__(self):
        self.client = salt.client.LocalClient()
        self.client.cmd('*','saltutil.sync_all')

    def getgrains(self,host_name,container):
        '''获得数据'''
        data = self.client.cmd(host_name, 'dockerinfo.inspect_container',[container] )
        return data

#数据库操作
class DbHelp(object):
    def __init__(self):
        self.host = '192.168.11.114'
        self.user = 'yuancheng'
        self.passwd = 'Aa_123@#'
        self.db = 'OMServer'
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

    def addHosts(self,name,sql):
        countsql='select * from jsh_hosts  where `name`="%s" ' % name
        count = self.cursor.execute(countsql)
        if count > 0:
            print "%s is exist" % name
        else:
            n = self.cursor.execute(sql)
            print "add %s" % name



    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class  Main(object):
    def main(self):
        '''主调函数'''
        dockerinfo = Dockerinfo()
        host_name = 'www.jsh315.com_master' #宿主机ID
        container_name = 'centos_mysql5.7' #容器ID
        items = dockerinfo.getgrains(host_name,container_name)
        for i in items:
            item = items[i]
            Ports =  item['NetworkSettings']['Ports']
            Port = "" #开放的端口
            for j in Ports:
                HostPort = Ports[j][0]['HostPort']
                LocalPort = j
                Port += '  '+ HostPort + '->'+ LocalPort

            IPAddress = item['NetworkSettings']['IPAddress'] #IP地址
            Created = str(item['Created'].split('.')[0].split('T')[0]) + ' ' + str(
                item['Created'].split('.')[0].split('T')[1])#该容器创建时间
            StartedAt=str(item['State']['StartedAt'].split('.')[0].split('T')[0]) + ' ' + str(
                item['State']['StartedAt'].split('.')[0].split('T')[1])#最近启动时间



if __name__ == '__main__':
    main_obj = Main()
    main_obj.main()
