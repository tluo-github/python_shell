#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         监控Docker容器运行情况
# Purpose:      使用docker-py获取所有被控机（CPU使用率、内存使用情况、磁盘使用情况、网络流量）插入数据库
# Version:      2.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------
import salt.client

import MySQLdb
import MySQLdb.cursors
import time
# 该类获得被控机器情况
class Dockerdata(object):
    def __init__(self):
        self.client = salt.client.LocalClient()


    def getcontainersdata(self):
        '''查询docker组'''
        data = self.client.cmd('docker','dockerinfo.stat_containers',expr_form='nodegroup')
        return data

# 数据库操作
class DbHelp(object):
    def __init__(self):
        self.host = '192.168.174.130'
        self.user = 'yuancheng'
        self.passwd = 'Aa_123@#'
        self.db = 'OMServer'
        self.charset = 'utf8'
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db,
                                    charset=self.charset, cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()


    def write_mysql(self, host_name,container_name,msg):
        #container_name = msg['Container_name']
        search_sql = "SELECT * from jsh_docker_containers WHERE host_name='%s' and  container_name='%s' limit 1" % (host_name,container_name)
        n = self.cursor.execute(search_sql)
        data = self.cursor.fetchall()
        for row in data:
            container_id = int(row['id'])
            insert_sql = "insert into jsh_docker_containers_data(container_id,container_name,cpu_percent,memory_usage,memory_limit,memory_percent,network_rx_packets,network_tx_packets,collect_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
                container_id, container_name, msg['Cpu_percent'], msg['Memory_usage'], msg['Memory_limit'],
                msg['Memory_percent'],
                msg['Network_rx_packets'], msg['Network_tx_packets'], msg['Collect_time'])
            # print insert_sql
            n = self.cursor.execute(insert_sql)
            if n <= 0:
                print "%s insert faild" % container_name
            else:
                self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class Main(object):
    def main(self):
        '''主调函数'''

        docker_data = Dockerdata()
        items = docker_data.getcontainersdata()
        db_help = DbHelp()

        for i in items:
            host_name = i
            item = items[i]
            for j in item:
                container_name = j
                msg = item[j]
                db_help.write_mysql(host_name,container_name,msg)

        db_help.close()

if __name__ == '__main__':
    start = time.clock()
    main_obj = Main()
    main_obj.main()
    end = time.clock()
    #print("The script run time is : %.03f seconds" % (end - start))