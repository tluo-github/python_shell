#!/usr/bin/env python
# coding=utf-8
# ----------------------------------------------------------
# Name:         监控Docker容器运行情况
# Purpose:      使用docker-py获取所有被控机（CPU使用率、内存使用情况、磁盘使用情况、网络流量）插入数据库
# Version:      1.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
#FileName:      docker_container_datas.py
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.6.6
# ----------------------------------------------------------

from docker import Client
import MySQLdb
import MySQLdb.cursors
import re
import json
#该类获得被控机器情况
class DockerHost(object):

    def __init__(self):
        '''初始化docker-py client'''
        self.docker_client = Client(base_url='unix://var/run/docker.sock',version='1.19')

    def docker_container_run(self):
        '''获取运行容器'''
        docker_container = self.docker_client.containers(all=True)
        container_name = []
        container_run_name = []
        for i in docker_container:
            if re.match('Up', i['Status']):
                container_name.append(i['Names'])
        for b in container_name:
            for c in b:
                container_run_name.append(c[1::])
        return container_run_name

    def check_container_stats(self,name):
        '''获得容器详细信息'''
        container_collect = self.docker_client.stats(name)
        old_result = json.loads(container_collect.next())
        new_result = json.loads(container_collect.next())
        container_collect.close()


        cpu_total_usage = new_result['cpu_stats']['cpu_usage']['total_usage']  -  old_result['cpu_stats']['cpu_usage'][ 'total_usage']
        cpu_system_uasge = new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
        cpu_num = len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
        cpu_percent = round((float(cpu_total_usage) / float(cpu_system_uasge)) * cpu_num * 100.0, 2)

        mem_usage = new_result['memory_stats']['usage']
        mem_limit = new_result['memory_stats']['limit']
        mem_percent = round(float(mem_usage) / float(mem_limit) * 100.0, 2)

        network_rx_packets = new_result['network']['rx_packets']
        network_tx_packets = new_result['network']['tx_packets']

        collect_time = str(new_result['read'].split('.')[0].split('T')[0]) + ' ' + str(
            new_result['read'].split('.')[0].split('T')[1])

        msg = {'Container_name': name,  #容器名称
               'Cpu_percent': cpu_percent, #CPU使用率
               'Memory_usage': mem_usage, #已使用内存
               'Memory_limit': mem_limit, #总内存
               'Memory_percent': mem_percent, #内存使用率
               'Network_rx_packets': network_rx_packets, #网络流入流量
               'Network_tx_packets': network_tx_packets, #网络流出流量
               'Collect_time': collect_time}
        return msg

#数据库操作
class DbHelp(object):
    def __init__(self):
        self.host = '192.168.11.114'
        self.user = 'yuancheng'
        self.passwd = 'Aa_123@#'
        self.db = 'OMServer'
        self.charset = 'utf8'
        self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset,cursorclass = MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def write_mysql(self,msg):
        container_name = msg['Container_name']
        search_sql = "SELECT * from jsh_docker_containers WHERE container_name='%s' limit 1" % container_name
        n = self.cursor.execute(search_sql)
        data = self.cursor.fetchall()
        for row in data:
            container_id = int(row['id'])
            insert_sql = "insert into jsh_docker_containers_data(container_id,cpu_percent,memory_usage,memory_limit,memory_percent,network_rx_packets,network_tx_packets,collect_time)values('%s','%s','%s','%s','%s','%s','%s','%s');" % (
            container_id, msg['Cpu_percent'], msg['Memory_usage'], msg['Memory_limit'], msg['Memory_percent'],
            msg['Network_rx_packets'], msg['Network_tx_packets'], msg['Collect_time'])
            n = self.cursor.execute(insert_sql)
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class  Main(object):
    def main(self):
        docker_host = DockerHost()
        docker_container_run_name = docker_host.docker_container_run()
        scan_result = []
        # 收集容器数据
        for i in docker_container_run_name:
            scan_result.append(docker_host.check_container_stats(i))

        db_help = DbHelp()
        for res in scan_result:
            #写入数据库
            db_help.write_mysql(res)

        db_help.close()
if __name__ == '__main__':
    main_obj = Main()
    main_obj.main()
