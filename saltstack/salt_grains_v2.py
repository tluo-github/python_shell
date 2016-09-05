#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         获取被控机静态数据脚本
# Purpose:      获取被控机静态数据(主机名(salt)、操作系统、系统内核、CPU核数、CPU型号、IP地址)
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
class hostinfo(object):
    def __init__(self):
        self.client = salt.client.LocalClient()
        self.client.cmd('*','saltutil.sync_all')

    def getgrains(self):
        '''获得数据'''
        grains = self.client.cmd('*', 'hostinfo.host_grains')
        return grains

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
        host = hostinfo()
        hostlist = host.getgrains()

        db_help = DbHelp()

        for i in hostlist:
            hostgrains = hostlist[i]
            name = i

            os = '%s-%s' % (hostgrains['osfinger']['osfinger'],hostgrains['osarch']['osarch'])
            kernel = '%s-%s' % (hostgrains['kernel']['kernel'],hostgrains['kernelrelease']['kernelrelease'])
            num_cpus = hostgrains['num_cpus']['num_cpus']
            cpu_model = hostgrains['cpu_model']['cpu_model']
            lo = hostgrains['ip4_interfaces']['ip4_interfaces']['lo'][0]
            eth0 = hostgrains['ip4_interfaces']['ip4_interfaces']['eth0'][0]
            mem_total = hostgrains['mem_total']['mem_total']

            insertSQL = 'insert into jsh_hosts (`name`,os,kernel,num_cpus,cpu_model,lo,eth0,createtime,mem_total) values("%s","%s","%s","%d","%s","%s","%s",now(),%d)' % (
            name, os, kernel, num_cpus, cpu_model, lo, eth0 , mem_total)
            #print insertSQL
            db_help.addHosts(name,insertSQL)

        db_help.close()
if __name__ == '__main__':
    main_obj = Main()
    main_obj.main()
